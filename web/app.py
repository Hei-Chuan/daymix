"""Small same-origin website API around the canonical Daymix Python engine."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "skills" / "daymix"))
from daymix import engine  # noqa: E402 — single canonical engine
from storage import SQLiteStorage  # noqa: E402

MAX_BODY = 4096
DAY_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
ZONE_PATTERN = re.compile(r"[A-Za-z0-9_+./-]{1,80}\Z")
ASSETS = {
    "/": (HERE / "public/index.html", "text/html; charset=utf-8"),
    "/app.js": (HERE / "public/app.js", "text/javascript; charset=utf-8"),
    "/styles.css": (HERE / "public/styles.css", "text/css; charset=utf-8"),
    "/favicon.svg": (ROOT / "skills/daymix/assets/icon.svg", "image/svg+xml"),
}


def handler_for(storage):
    class Handler(BaseHTTPRequestHandler):
        server_version = "DaymixWeb/1"

        def log_message(self, *_args):
            # Never log bearer tokens, recovery codes, request bodies or histories.
            pass

        def headers_common(self):
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")

        def respond(self, status: int, payload: dict):
            data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.headers_common()
            self.end_headers()
            self.wfile.write(data)

        def body(self):
            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise ValueError("请求格式不正确")
            if size < 0 or size > MAX_BODY:
                raise ValueError("请求太大")
            try:
                value = json.loads(self.rfile.read(size)) if size else {}
            except (UnicodeDecodeError, json.JSONDecodeError):
                raise ValueError("请求格式不正确")
            if not isinstance(value, dict):
                raise ValueError("请求格式不正确")
            return value

        def user(self):
            auth = self.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return None
            return storage.user_for_token(auth[7:])

        def require_user(self):
            user_id = self.user()
            if not user_id:
                self.respond(401, {"error": "请重新打开页面以恢复本机身份"})
            return user_id

        def do_GET(self):
            path = urlsplit(self.path)
            if path.path == "/healthz":
                self.respond(200, {"status": "ok"})
                return
            if path.path in ASSETS:
                filename, content_type = ASSETS[path.path]
                data = filename.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.headers_common()
                self.end_headers()
                self.wfile.write(data)
                return
            if path.path == "/api/history":
                user_id = self.require_user()
                if user_id:
                    self.respond(200, {"items": storage.history(user_id)})
                return
            if path.path == "/api/drop":
                user_id = self.require_user()
                if not user_id:
                    return
                day = parse_qs(path.query).get("date", [""])[0]
                if not DAY_PATTERN.fullmatch(day):
                    self.respond(400, {"error": "日期格式不正确"})
                    return
                ledger = storage.saved_drop(user_id, day)
                if ledger:
                    self.respond(200, {"ledger": ledger})
                else:
                    self.respond(404, {"error": "这张卡没有保存"})
                return
            self.respond(404, {"error": "未找到页面"})

        def do_POST(self):
            path = urlsplit(self.path).path
            if path not in ("/api/session", "/api/drop", "/api/sync", "/api/restore"):
                self.respond(404, {"error": "未找到接口"})
                return
            try:
                data = self.body()
                if path == "/api/session":
                    _user_id, token = storage.create_user()
                    self.respond(201, {"token": token})
                    return
                if path == "/api/restore":
                    code = data.get("code", "")
                    if not isinstance(code, str) or len(code) > 128:
                        raise ValueError("同步码不正确")
                    restored = storage.restore(code)
                    if restored:
                        self.respond(200, {"token": restored[1]})
                    else:
                        self.respond(400, {"error": "同步码不正确"})
                    return
                user_id = self.require_user()
                if not user_id:
                    return
                if path == "/api/sync":
                    self.respond(200, {"code": storage.create_recovery_code(user_id)})
                    return
                timezone_name = data.get("timezone", "Asia/Shanghai")
                if not isinstance(timezone_name, str) or not ZONE_PATTERN.fullmatch(timezone_name):
                    raise ValueError("时区不正确")
                try:
                    zone = ZoneInfo(timezone_name)
                except (ZoneInfoNotFoundError, ValueError):
                    raise ValueError("时区不正确")
                today = datetime.now(zone).date()
                ledger = storage.get_or_create_drop(user_id, today.isoformat(), timezone_name,
                                                    lambda: engine.make(today, timezone_name, user_id))
                self.respond(200, {"ledger": ledger})
            except ValueError as exc:
                self.respond(400, {"error": str(exc)})
            except Exception:
                self.respond(503, {"error": "暂时没能打开日卡，请稍后再试"})

    return Handler


def main():
    database = Path(os.environ.get("DAYMIX_WEB_DB", str(HERE / "data" / "daymix.sqlite3")))
    storage = SQLiteStorage(database)
    host = os.environ.get("DAYMIX_WEB_HOST", "127.0.0.1")
    port = int(os.environ.get("DAYMIX_WEB_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), handler_for(storage))
    print(f"Daymix website: http://{host}:{server.server_port}/", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

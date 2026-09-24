"""Website-only persistence; the Daymix engine does not import this module."""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Protocol


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def token_hash(token: str) -> str:
    # Tokens have 256 bits of entropy. A fast hash is safe for indexed lookup.
    return hashlib.sha256(token.encode("ascii")).hexdigest()


class Storage(Protocol):
    def create_user(self) -> tuple[str, str]: ...
    def user_for_token(self, token: str) -> str | None: ...
    def create_recovery_code(self, user_id: str) -> str: ...
    def restore(self, code: str) -> tuple[str, str] | None: ...
    def get_or_create_drop(self, user_id: str, day: str, timezone_name: str,
                           generate: Callable[[], dict]) -> dict: ...
    def history(self, user_id: str) -> list[dict]: ...
    def saved_drop(self, user_id: str, day: str) -> dict | None: ...


class SQLiteStorage:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS anonymous_users (
                    id TEXT PRIMARY KEY,
                    recovery_salt BLOB,
                    recovery_hash BLOB,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS devices (
                    token_hash TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES anonymous_users(id),
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS daily_drops (
                    user_id TEXT NOT NULL REFERENCES anonymous_users(id),
                    date TEXT NOT NULL,
                    timezone TEXT NOT NULL,
                    cast_version TEXT NOT NULL,
                    data_version TEXT NOT NULL,
                    ledger_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (user_id, date)
                );
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=5000")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def create_user(self) -> tuple[str, str]:
        user_id = secrets.token_hex(12)
        token = secrets.token_urlsafe(32)
        with self.connect() as db:
            db.execute("INSERT INTO anonymous_users(id, created_at) VALUES (?, ?)", (user_id, now_utc()))
            db.execute("INSERT INTO devices(token_hash, user_id, created_at) VALUES (?, ?, ?)",
                       (token_hash(token), user_id, now_utc()))
        return user_id, token

    def user_for_token(self, token: str) -> str | None:
        if not token or len(token) > 128:
            return None
        try:
            digest = token_hash(token)
        except UnicodeEncodeError:
            return None
        with self.connect() as db:
            row = db.execute("SELECT user_id FROM devices WHERE token_hash=?", (digest,)).fetchone()
        return row[0] if row else None

    def create_recovery_code(self, user_id: str) -> str:
        secret = secrets.token_hex(20)  # 160 bits; copy/paste rather than memorization.
        code = f"dmx1.{user_id}.{secret}"
        salt = secrets.token_bytes(16)
        digest = hashlib.scrypt(code.encode("ascii"), salt=salt, n=16384, r=8, p=1)
        with self.connect() as db:
            result = db.execute("UPDATE anonymous_users SET recovery_salt=?, recovery_hash=? WHERE id=?",
                                (salt, digest, user_id))
            if result.rowcount != 1:
                raise ValueError("unknown user")
        return code

    def restore(self, code: str) -> tuple[str, str] | None:
        parts = code.strip().split(".")
        if len(parts) != 3 or parts[0] != "dmx1" or len(parts[1]) != 24 or len(parts[2]) != 40:
            return None
        if any(c not in "0123456789abcdef" for c in parts[1] + parts[2]):
            return None
        user_id = parts[1]
        with self.connect() as db:
            row = db.execute("SELECT recovery_salt, recovery_hash FROM anonymous_users WHERE id=?", (user_id,)).fetchone()
            if not row or not row[0] or not row[1]:
                return None
            digest = hashlib.scrypt(code.encode("ascii"), salt=row[0], n=16384, r=8, p=1)
            if not hmac.compare_digest(digest, row[1]):
                return None
            token = secrets.token_urlsafe(32)
            db.execute("INSERT INTO devices(token_hash, user_id, created_at) VALUES (?, ?, ?)",
                       (token_hash(token), user_id, now_utc()))
        return user_id, token

    def get_or_create_drop(self, user_id: str, day: str, timezone_name: str,
                           generate: Callable[[], dict]) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT ledger_json FROM daily_drops WHERE user_id=? AND date=?", (user_id, day)).fetchone()
            if row:
                return json.loads(row[0])
        ledger = generate()
        encoded = json.dumps(ledger, ensure_ascii=False, separators=(",", ":"))
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO daily_drops(user_id,date,timezone,cast_version,data_version,ledger_json,created_at) VALUES (?,?,?,?,?,?,?)",
                       (user_id, day, timezone_name, ledger["cast_version"], ledger["data_version"], encoded, now_utc()))
            row = db.execute("SELECT ledger_json FROM daily_drops WHERE user_id=? AND date=?", (user_id, day)).fetchone()
        return json.loads(row[0])

    def history(self, user_id: str) -> list[dict]:
        with self.connect() as db:
            rows = db.execute("SELECT date,timezone,cast_version,data_version,ledger_json,created_at FROM daily_drops WHERE user_id=? ORDER BY date DESC", (user_id,)).fetchall()
        return [{"date":day,"timezone":tz,"cast_version":cast,"data_version":data,
                 "rating":json.loads(ledger)["rating"]["rating"],"created_at":created}
                for day,tz,cast,data,ledger,created in rows]

    def saved_drop(self, user_id: str, day: str) -> dict | None:
        with self.connect() as db:
            row = db.execute("SELECT ledger_json FROM daily_drops WHERE user_id=? AND date=?", (user_id, day)).fetchone()
        return json.loads(row[0]) if row else None

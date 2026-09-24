"""Website state guarantees: immutable ledgers, anonymous restore and API isolation."""
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "web"))
from app import handler_for  # noqa: E402
from storage import SQLiteStorage  # noqa: E402


class WebTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "daymix.sqlite3"
        self.storage = SQLiteStorage(self.database)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.storage))
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join(timeout=2)
        self.temp.cleanup()

    def request(self, path, *, method="GET", token=None, body=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        request = Request(self.base + path, data=json.dumps(body).encode() if body is not None else None,
                          headers=headers, method=method)
        try:
            with urlopen(request, timeout=10) as response:
                return response.status, json.load(response)
        except HTTPError as exc:
            return exc.code, json.load(exc)

    def test_history_is_saved_ledger_and_restore_joins_same_identity(self):
        _, first = self.request("/api/session", method="POST", body={})
        original_token = first["token"]
        status, result = self.request("/api/drop", method="POST", token=original_token,
                                      body={"timezone": "Asia/Shanghai"})
        self.assertEqual(status, 200)
        ledger = result["ledger"]
        self.assertEqual(ledger["cast_version"], "v2.2")
        day = ledger["date"]["gregorian"]
        # Re-opening the day must read stored JSON without invoking the engine again.
        _, second = self.request("/api/drop", method="POST", token=original_token,
                                 body={"timezone": "Asia/Shanghai"})
        self.assertEqual(second["ledger"], ledger)
        user_id = self.storage.user_for_token(original_token)
        stored = self.storage.get_or_create_drop(user_id, day, "UTC",
                                                  lambda: self.fail("saved card was recalculated"))
        self.assertEqual(stored, ledger)
        _, sync = self.request("/api/sync", method="POST", token=original_token, body={})
        code = sync["code"]
        self.assertNotIn(code.encode(), self.database.read_bytes())
        _, other = self.request("/api/session", method="POST", body={})
        self.assertEqual(self.request(f"/api/drop?date={day}", token=other["token"])[0], 404)
        _, restored = self.request("/api/restore", method="POST", body={"code": code})
        self.assertNotEqual(restored["token"], original_token)
        self.assertEqual(self.request(f"/api/drop?date={day}", token=restored["token"])[1]["ledger"], ledger)
        self.assertEqual(len(self.request("/api/history", token=restored["token"])[1]["items"]), 1)
        self.assertEqual(self.request(f"/api/drop?date={day}")[0], 401)
        self.assertEqual(self.request("/api/restore", method="POST", body={"code": code + "0"})[0], 400)
        self.request("/api/sync", method="POST", token=restored["token"], body={})
        self.assertEqual(self.request("/api/restore", method="POST", body={"code": code})[0], 400)

    def test_static_site_and_health_are_available_without_identity(self):
        status, health = self.request("/healthz")
        self.assertEqual((status, health["status"]), (200, "ok"))
        with urlopen(self.base + "/", timeout=5) as response:
            page = response.read().decode("utf-8")
        self.assertIn("今天掉落了什么", page)
        self.assertIn("/app.js", page)


if __name__ == "__main__":
    unittest.main()

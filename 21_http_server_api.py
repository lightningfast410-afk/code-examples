"""21_http_server_api.py — A tiny REST-style API on the standard library.

Demonstrates: http.server with JSON in and out, proper status
codes (200, 201, 404, 400), and a test client in the same file
that exercises the API over localhost and shuts the server
down. No external network is used; the server binds 127.0.0.1
on an ephemeral port.
Run: python3 21_http_server_api.py
"""

import json
import threading
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ITEMS = {}
NEXT_ID = [1]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep the demo output clean

    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/items":
            return self._send(200, list(ITEMS.values()))
        if self.path.startswith("/items/"):
            try:
                item_id = int(self.path.split("/")[-1])
            except ValueError:
                return self._send(400, {"error": "id must be an integer"})
            if item_id in ITEMS:
                return self._send(200, ITEMS[item_id])
            return self._send(404, {"error": "not found"})
        return self._send(404, {"error": "unknown route"})

    def do_POST(self):
        if self.path != "/items":
            return self._send(404, {"error": "unknown route"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length) or b"{}")
            name = data["name"]
        except (ValueError, KeyError):
            return self._send(400, {"error": "body must be JSON with a name"})
        item = {"id": NEXT_ID[0], "name": name}
        NEXT_ID[0] += 1
        ITEMS[item["id"]] = item
        return self._send(201, item)


def request(port, method, path, body=None):
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    headers = {"Content-Type": "application/json"} if body is not None else {}
    conn.request(method, path,
                 body=json.dumps(body) if body is not None else None,
                 headers=headers)
    resp = conn.getresponse()
    data = json.loads(resp.read() or b"{}")
    conn.close()
    return resp.status, data


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        status, created = request(port, "POST", "/items", {"name": "widget"})
        assert status == 201 and created["id"] == 1
        status, found = request(port, "GET", "/items/1")
        assert status == 200 and found["name"] == "widget"
        status, missing = request(port, "GET", "/items/99")
        assert status == 404
        status, bad = request(port, "POST", "/items", {"wrong": True})
        assert status == 400
    finally:
        server.shutdown()
    print("PROOF: POST 201, GET 200, missing 404, bad body 400")


if __name__ == "__main__":
    main()

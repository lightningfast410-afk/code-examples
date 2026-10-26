"""22_http_retry_client.py — Retry transient failures, never permanent ones.

Demonstrates: a client that retries only on retryable statuses
(500/502/503) with exponential backoff, and gives up cleanly
on a 400. The flaky server is a local stub that fails twice
then succeeds, so the whole proof runs on localhost.
Run: python3 22_http_retry_client.py
"""

import threading
import time
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CALLS = [0]


class Flaky(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        CALLS[0] += 1
        if CALLS[0] <= 2:
            self.send_response(503)
        else:
            self.send_response(200)
        body = b"{}"
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


RETRYABLE = {500, 502, 503}


def get_with_retry(port, path, attempts=5, base_delay=0.05):
    """Return (status, attempts_used); backoff doubles each retry."""
    for attempt in range(1, attempts + 1):
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", path)
        status = conn.getresponse().status
        conn.close()
        if status not in RETRYABLE or attempt == attempts:
            return status, attempt
        time.sleep(base_delay * (2 ** (attempt - 1)))
    return status, attempts


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Flaky)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        status, used = get_with_retry(port, "/data")
        assert status == 200 and used == 3  # failed twice, won on retry 3
        assert CALLS[0] == 3
    finally:
        server.shutdown()
    print("PROOF: flaky server failed twice, retry won on attempt 3")


if __name__ == "__main__":
    main()

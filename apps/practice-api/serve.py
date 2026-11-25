# Runs the practice enrolment API (app.py) as a real HTTP server on your own computer.
# Standard library only. Start it with:  python serve.py   and stop it with Ctrl+C.
# POST /reset puts the starting data back (the tests' fake_api.Session() calls it).
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qsl, urlsplit

import app

HOST, PORT = "127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(BaseHTTPRequestHandler):
    def answer(self, method):
        parts = urlsplit(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if method == "POST" and parts.path == "/reset":
            app.reset()
            return self.send(204, None, {})
        try:
            body = json.loads(raw) if raw else None
        except ValueError:
            return self.send(400, {"error": "The body is not valid JSON."}, {})
        result = app.handle(method, parts.path, dict(parse_qsl(parts.query)), body, dict(self.headers))
        self.send(result[0], result[1], result[2] if len(result) > 2 else {})

    def send(self, status, body, extra):
        data = b"" if body is None else json.dumps(body).encode()
        self.send_response(status)
        if body is not None:
            self.send_header("Content-Type", "application/json")
        for key, value in extra.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self.answer("GET")

    def do_POST(self):
        self.answer("POST")

    def do_PUT(self):
        self.answer("PUT")

    def do_PATCH(self):
        self.answer("PATCH")

    def do_DELETE(self):
        self.answer("DELETE")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    app.reset()
    print(f"Practice API on http://{HOST}:{PORT} (Ctrl+C to stop)", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()

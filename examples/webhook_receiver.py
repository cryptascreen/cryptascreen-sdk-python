"""Minimal webhook receiver that verifies the signature (stdlib http.server; test secret from the environment)."""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from cryptascreen import WebhookSignatureError, construct_webhook_event

SECRET = os.environ["CRYPTASCREEN_WEBHOOK_SECRET"]


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        try:
            event = construct_webhook_event(SECRET, raw, dict(self.headers.items()))
        except WebhookSignatureError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(e.code.encode())
            return
        print(event["type"], event["data"].get("evaluationId"))
        self.send_response(200)
        self.end_headers()


HTTPServer(("127.0.0.1", 8099), Handler).serve_forever()

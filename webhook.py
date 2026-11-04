from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import payments


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/yookassa":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        signature = self.headers.get("Signature", "")
        ok = payments.process_notification(body, signature)
        self.send_response(200 if ok else 403)
        self.end_headers()
        self.wfile.write(b"ok" if ok else b"bad signature")

    def log_message(self, *args):
        pass  # не пишем тело запроса в логи


def run(port=8000):
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    run()

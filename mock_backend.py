"""Локальный мок-бэкенд: принимает заявку и печатает её (для теста пути сайт -> бэкенд)."""
import json, sys, http.server
sys.stdout.reconfigure(encoding="utf-8")


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n).decode("utf-8", "ignore")
        print("=== POST %s" % self.path)
        print("    content-type:", self.headers.get("Content-Type"))
        print("    body:", raw, flush=True)
        try:
            d = json.loads(raw)
            print("    parsed phone:", d.get("phone"), "| name:", d.get("name"), flush=True)
        except Exception as e:
            print("    parse err:", e, flush=True)
        body = b'{"ok":true}'
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8126), H).serve_forever()

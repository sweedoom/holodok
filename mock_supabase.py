"""Мок Supabase REST — чтобы проверить админку без реального проекта."""
import json, sys, http.server
from urllib.parse import urlparse
sys.stdout.reconfigure(encoding="utf-8")

LEADS = [
    {"id": "11111111-1111-1111-1111-111111111111",
     "created_at": "2026-09-16T00:52:00.000Z", "name": "Алексей Петров",
     "phone": "+7 (912) 345-67-89", "message": "Парогенератор Tylo не включается",
     "source": "Главная форма", "page": "http://linar.me/holodok/",
     "status": "new", "comment": "", "utm": ""},
    {"id": "22222222-2222-2222-2222-222222222222",
     "created_at": "2026-09-15T21:40:00.000Z", "name": "Мария Иванова",
     "phone": "+7 (982) 111-22-33", "message": "Сколько стоит замена ТЭНа?",
     "source": "Модальная форма", "page": "http://linar.me/holodok/",
     "status": "work", "comment": "Согласовали 7500, мастер едет завтра", "utm": ""},
    {"id": "33333333-3333-3333-3333-333333333333",
     "created_at": "2026-09-15T18:12:00.000Z", "name": "",
     "phone": "+7 (905) 000-11-22", "message": "", "source": "Модальная форма",
     "page": "http://linar.me/holodok/#price", "status": "new", "comment": "", "utm": ""},
    {"id": "44444444-4444-4444-4444-444444444444",
     "created_at": "2026-09-15T14:05:00.000Z", "name": "Дмитрий Сергеевич",
     "phone": "+7 (999) 584-43-58", "message": "Замена помпы Tylo Combi 7",
     "source": "Главная форма", "page": "http://linar.me/holodok/",
     "status": "done", "comment": "Оплачено 8500", "utm": ""},
    {"id": "55555555-5555-5555-5555-555555555555",
     "created_at": "2026-09-14T11:23:00.000Z", "name": "Ирина",
     "phone": "+7 (351) 900-12-34", "message": "", "source": "Главная форма",
     "page": "http://linar.me/holodok/", "status": "cancel",
     "comment": "Передумали", "utm": ""},
]


class H(http.server.BaseHTTPRequestHandler):
    def _c(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")

    def do_OPTIONS(self):
        self.send_response(200); self._c(); self.end_headers()

    def do_GET(self):
        p = urlparse(self.path).path
        if p.endswith("/rest/v1/leads"):
            body = json.dumps(LEADS, ensure_ascii=False).encode()
            self.send_response(200); self._c()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
        else:
            self.send_response(404); self._c(); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n).decode("utf-8", "ignore")
        print("POST lead:", raw[:200], flush=True)
        self.send_response(201); self._c(); self.end_headers()

    def do_PATCH(self):
        print("PATCH:", self.path, flush=True)
        self.send_response(204); self._c(); self.end_headers()

    def do_DELETE(self):
        print("DELETE:", self.path, flush=True)
        self.send_response(204); self._c(); self.end_headers()

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8140), H).serve_forever()
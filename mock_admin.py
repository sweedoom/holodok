"""Мок-бэкенд админки: отдаёт JSONP со списком заявок (для превью админки)."""
import json, sys, http.server
sys.stdout.reconfigure(encoding="utf-8")

PW = "demo1234"
LEADS = [
    {"date":"2026-09-15 21:18:02","id":"a1b2c3d4","name":"Алексей Петров","phone":"+7 (912) 345-67-89",
     "message":"Парогенератор Tylo не включается, мигает индикатор","source":"Главная форма",
     "page":"http://linar.me/holodok/","status":"new","comment":"","utm":""},
    {"date":"2026-09-15 18:42:11","id":"e5f6g7h8","name":"Мария Иванова","phone":"+7 (982) 111-22-33",
     "message":"Сколько стоит замена ТЭНа?","source":"Модальная форма","page":"http://linar.me/holodok/",
     "status":"work","comment":"Согласовали 7500₽, мастер выезжает завтра","utm":""},
    {"date":"2026-09-15 14:09:55","id":"i9j0k1l2","name":"","phone":"+7 (905) 000-11-22","message":"",
     "source":"Модальная форма","page":"http://linar.me/holodok/#price","status":"new","comment":"","utm":""},
    {"date":"2026-09-14 11:23:40","id":"m3n4o5p6","name":"Дмитрий Сергеевич","phone":"+7 (999) 584-43-58",
     "message":"Замена помпы Tylo Combi 7","source":"Главная форма","page":"http://linar.me/holodok/",
     "status":"done","comment":"Оплачено 8500₽","utm":""},
    {"date":"2026-09-14 09:01:17","id":"q7r8s9t0","name":"Ирина","phone":"+7 (351) 900-12-34","message":"",
     "source":"Главная форма","page":"http://linar.me/holodok/","status":"cancel","comment":"Передумали","utm":""},
]


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
    def _send_jsonp(self, body, cb):
        out = (cb + "(" + json.dumps(body, ensure_ascii=False) + ")").encode("utf-8")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        action = (q.get("action") or ["ping"])[0]
        cb = (q.get("callback") or [""])[0]

        if action == "ping": return self._send_jsonp({"ok": True, "service": "leads"}, cb)
        if (q.get("pw") or [""])[0] != PW:
            return self._send_jsonp({"ok": False, "error": "Неверный пароль"}, cb)

        if action == "list":
            return self._send_jsonp({"ok": True, "leads": LEADS}, cb)
        if action in ("status", "comment", "delete"):
            return self._send_jsonp({"ok": True, "done": True}, cb)
        return self._send_jsonp({"ok": False, "error": "unknown action"}, cb)

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8127), H).serve_forever()
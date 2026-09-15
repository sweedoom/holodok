import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        results = []
        pg.on("dialog", lambda d: asyncio.ensure_future(d.dismiss()))
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        # перехватываем ответы от Telegram
        posts = []

        async def on_resp(resp):
            if "api.telegram.org" in resp.url:
                try:
                    body = await resp.text()
                except Exception:
                    body = "?"
                results.append((resp.status, body[:200]))
        pg.on("response", lambda r: asyncio.ensure_future(on_resp(r)))
        pg.on("request", lambda r: posts.append(r.url) if r.method == "POST" else None)

        await pg.goto("http://127.0.0.1:8129/index.html", wait_until="load", timeout=60000) \
            if False else None
        # работаем с локальной сборкой
        import http.server, threading, functools, os
        os.chdir(r"G:\SlavaSaitOffer\site\docs")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler)
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8131), handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()

        await pg.goto("http://127.0.0.1:8131/index.html", wait_until="load", timeout=60000)
        await pg.wait_for_timeout(2500)
        await pg.fill("#phone-main", "+7 (999) 111-22-33")
        await pg.click(".form-btn >> nth=0")
        await pg.wait_for_timeout(3500)

        print("=== POST-запросы ===")
        for u in posts:
            print("  ", u[:110])
        print("=== ответы Telegram ===")
        for st, body in results:
            print(f"  status={st}  {body}")
        print("errors:", errs[:3])
        await b.close()

asyncio.run(main())
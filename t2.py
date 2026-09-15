import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        posts, resps = [], []
        pg.on("dialog", lambda d: asyncio.ensure_future(d.dismiss()))
        pg.on("request", lambda r: posts.append(r.url) if r.method == "POST" else None)

        async def on_resp(r):
            if "api.telegram.org" in r.url:
                try:
                    resps.append((r.status, (await r.text())[:130]))
                except Exception as e:
                    resps.append((0, str(e)[:80]))
        pg.on("response", lambda r: asyncio.ensure_future(on_resp(r)))

        await pg.goto("http://127.0.0.1:8133/index.html", wait_until="load", timeout=60000)
        await pg.wait_for_timeout(2500)
        await pg.fill("#phone-main", "+7 (999) 111-22-33")
        await pg.click(".form-btn >> nth=0")
        await pg.wait_for_timeout(4000)
        print("POST к Telegram:", len([u for u in posts if "telegram" in u]))
        for u in posts:
            if "telegram" in u:
                print("   ", u[-60:])
        print("ответы:")
        for st, body in resps:
            print(f"   {st}  {body}")
        await b.close()

asyncio.run(main())
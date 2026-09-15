import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        posts = []
        pg.on("request", lambda r: posts.append((r.method, r.url)) if r.method == "POST" else None)
        pg.on("dialog", lambda d: asyncio.ensure_future(d.dismiss()))
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://linar.me/holodok/", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(3000)
        await pg.fill("#phone-main", "+7 (351) 200-40-40")
        await pg.click(".form-btn >> nth=0")
        await pg.wait_for_timeout(2500)
        print("LIVE POSTS:", posts)
        print("errors:", errs[:3])
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\live_after.png")
        await b.close()

asyncio.run(main())
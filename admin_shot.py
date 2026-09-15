import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://127.0.0.1:8125/admin.html", wait_until="load", timeout=30000)
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\admin_shot.png", full_page=True)
        print("errors:", errs[:3])
        await b.close()

asyncio.run(main())
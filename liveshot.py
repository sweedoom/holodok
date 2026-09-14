import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8")

URL = "http://linar.me/holodok/"
OUT = r"G:\SlavaSaitOffer\site"

async def main():
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: errs.append("FAIL " + r.url[:80]))
        await pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(3000)
        for x in (0.3, 0.6, 1.0):
            await pg.evaluate(f"window.scrollTo(0, document.body.scrollHeight*{x})")
            await pg.wait_for_timeout(800)
        await pg.evaluate("window.scrollTo(0,0)")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=f"{OUT}\\live.png", full_page=False)
        await pg.screenshot(path=f"{OUT}\\live_full.png", full_page=True)
        title = await pg.title()
        print("LIVE TITLE:", title)
        print("LIVE URL final:", URL)
        print("ERRORS:", len(errs))
        for e in errs[:8]: print("  ", e[:160])
        await b.close()

asyncio.run(main())
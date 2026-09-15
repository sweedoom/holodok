import asyncio, sys
from playwright.async_api import async_playwright
sys.stdout.reconfigure(encoding="utf-8")

URL = "http://127.0.0.1:8141/admin-a7f3c9.html"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL, wait_until="domcontentloaded", timeout=30000)
        await pg.wait_for_timeout(1500)
        await pg.fill("#pw", "holodok2026")
        await pg.click("#go")
        await pg.wait_for_timeout(2500)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\sb_admin.png")
        rows = await pg.evaluate("document.querySelectorAll('#rows tr').length")
        stats = await pg.evaluate("document.getElementById('stats').innerText.replace(/\\n/g,' | ')")
        print("строк в таблице:", rows)
        print("статистика:", stats)
        # открыть карточку
        await pg.evaluate("document.querySelectorAll('#rows tr')[0].click()")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\sb_modal.png")
        print("errors:", errs[:3])
        await b.close()

asyncio.run(main())
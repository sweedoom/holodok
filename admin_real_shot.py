import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1360, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://127.0.0.1:8125/admin.html", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(3000)
        # screenshot first
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\admin_state.png")
        # then try login
        await pg.fill("#pw", "demo1234", timeout=10000)
        await pg.click("#go")
        await pg.wait_for_timeout(3000)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\admin_logged.png", full_page=False)
        # кликнем первую заявку, чтобы открылся диалог
        await pg.evaluate("document.querySelectorAll('#rows tr')[0].click()")
        await pg.wait_for_timeout(700)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\admin_modal.png", full_page=False)
        print("errors:", errs[:3])
        await b.close()

asyncio.run(main())
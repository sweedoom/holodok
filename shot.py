import sys, asyncio
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:8124/index.html"
OUT = r"G:\SlavaSaitOffer\site"

async def shoot(pg, name, w, h):
    await pg.set_viewport_size({"width": w, "height": h})
    await pg.goto(URL, wait_until="load", timeout=60000)
    await pg.wait_for_timeout(2500)
    # скролл чтобы грузить lazy
    for x in (0.3, 0.6, 1.0):
        await pg.evaluate(f"window.scrollTo(0, document.body.scrollHeight*{x})")
        await pg.wait_for_timeout(800)
    await pg.evaluate("window.scrollTo(0, 0)")
    await pg.wait_for_timeout(500)
    await pg.screenshot(path=f"{OUT}\\{name}.png", full_page=False)
    await pg.screenshot(path=f"{OUT}\\{name}_full.png", full_page=True)

async def main():
    errs, fails = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: fails.append(r.url + " :: " + str(r.failure)))
        await shoot(pg, "preview", 1440, 900)
        await shoot(pg, "preview_mobile", 390, 844)
        title = await pg.title()
        print("TITLE:", title)
        print("CONSOLE ERRORS:", len(errs))
        for e in errs[:8]: print("  ", e[:180])
        print("FAILED REQUESTS:", len(fails))
        for f in fails[:8]: print("  ", f[:180])
        await b.close()

asyncio.run(main())
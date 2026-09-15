import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        errs = []
        msgs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: msgs.append(m.type + ":" + m.text))
        await pg.goto("http://127.0.0.1:8125/admin.html?nocache=" + str(asyncio.get_event_loop().time()), wait_until="domcontentloaded")
        await pg.wait_for_timeout(2000)
        r = await pg.evaluate("({hasPw: !!document.getElementById('pw'), hasSetup: !!document.querySelector('.setup'), backend: window.BACKEND})")
        print("state:", r)
        print("errors:", errs[:5])
        print("console:")
        for m in msgs[:10]: print("  ", m[:150])
        await b.close()

asyncio.run(main())
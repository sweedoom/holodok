import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto("http://linar.me/holodok/", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(3000)
        await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await pg.wait_for_timeout(1500)
        f = await pg.query_selector("footer")
        if f:
            await f.scroll_into_view_if_needed()
            await pg.wait_for_timeout(500)
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\qa_footer.png")
        ct = await pg.evaluate("()=>{const d=document.querySelector('.address-text'); return d?d.innerText:null}")
        print("address-text:", repr(ct))
        await b.close()

asyncio.run(main())
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1360,"height":900})
        errors=[]; pg.on("pageerror",lambda e:errors.append(str(e)))
        await pg.goto("http://127.0.0.1:8142/admin-a7f3c9.html",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(1200)
        await pg.fill("#pw","holodok2026")
        await pg.click("#go")
        await pg.wait_for_timeout(2500)
        rows=await pg.evaluate("document.querySelectorAll('#rows tr').length")
        stats=await pg.evaluate("document.querySelector('#stats')?.innerText")
        print("rows:",rows)
        print("stats:",repr(stats))
        await pg.screenshot(path=r"G:\SlavaSaitOffer\site\real_admin.png")
        # открыть первую карточку and save comment/status
        if rows:
            await pg.evaluate("document.querySelector('#rows tr').click()")
            await pg.wait_for_timeout(300)
            print("modal:",await pg.locator("#ov").get_attribute("class"))
        print("errors:",errors[:3])
        await b.close()

asyncio.run(main())
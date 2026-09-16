import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1440,"height":900})
        posts=[]; responses=[]; errors=[]
        pg.on("request",lambda r: posts.append(r.url) if r.method=="POST" else None)
        pg.on("pageerror",lambda e:errors.append(str(e)))
        async def resp(r):
            if "supabase.co" in r.url or "api.telegram.org" in r.url:
                responses.append((r.status,r.url))
        pg.on("response",lambda r:asyncio.ensure_future(resp(r)))
        await pg.goto("http://127.0.0.1:8142/index.html",wait_until="load",timeout=60000)
        await pg.wait_for_timeout(1500)
        await pg.fill("#phone-main","+7 (999) 555-44-33")
        await pg.click(".form-btn >> nth=0")
        await pg.wait_for_timeout(4500)
        print("POST supabase:",len([x for x in posts if 'supabase.co' in x]))
        print("POST telegram:",len([x for x in posts if 'api.telegram.org' in x]))
        print("responses:")
        for x in responses: print(" ",x)
        print("errors:",errors[:3])
        await b.close()

asyncio.run(main())
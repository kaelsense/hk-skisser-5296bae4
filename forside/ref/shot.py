import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for name,url in [('heikampen','https://heikampen.no/'),('harvest','https://www.harvestmagazine.no/'),('nasjonalmuseet','https://www.nasjonalmuseet.no/')]:
            pg=await b.new_page(viewport={'width':1440,'height':900})
            try:
                await pg.goto(url,wait_until='networkidle',timeout=45000)
            except Exception as e: print(name,e)
            await pg.wait_for_timeout(2500)
            await pg.screenshot(path=f'{name}.png')
            await pg.screenshot(path=f'{name}-full.png',full_page=True)
            fonts=await pg.evaluate("""()=>{const s=new Set();document.querySelectorAll('h1,h2,h3,p,a,body').forEach(e=>{const c=getComputedStyle(e);s.add(e.tagName+': '+c.fontFamily+' '+c.fontSize+' '+c.color+' bg '+c.backgroundColor)});return [...s].slice(0,25)}""")
            print(name); [print('  ',f) for f in fonts]
        await b.close()
asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright
B='file:///workspace/heikampen/redesign/forside/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        jobs=[('index.html',1440,900,'forside-desktop.png',True,False),('index.html',1440,900,'forside-desktop-topp.png',False,False),('index.html',390,844,'forside-mobil.png',True,True)]
        jobs+=[(f'hero-test-{n}.html',1440,900,f'forside-hero-test-{n}.png',False,False) for n in (1,2,3)]
        jobs+=[('hero-test-3.html',390,844,'/tmp/t3m.png',False,True),('index.html',1024,768,'/tmp/tab.png',True,False)]
        for f,w,h,out,full,mob in jobs:
            c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=2 if mob else 1,is_mobile=mob,has_touch=mob)
            pg=await c.new_page(); await pg.goto(B+f,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
            print(out,await pg.evaluate('document.documentElement.scrollWidth'),await pg.evaluate('[...document.images].filter(i=>!i.naturalWidth).length'))
            await pg.screenshot(path=out,full_page=full); await c.close()
        await b.close()
asyncio.run(main())

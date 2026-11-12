import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        url='file:///workspace/heikampen/redesign/forside/index.html'
        for w,h,name,full,mob in [(1440,900,'forside-desktop.png',True,False),(1440,900,'forside-desktop-topp.png',False,False),(390,844,'forside-mobil.png',True,True)]:
            c=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1 if not mob else 2,is_mobile=mob,has_touch=mob)
            pg=await c.new_page(); await pg.goto(url,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
            ov=await pg.evaluate('document.documentElement.scrollWidth')
            broken=await pg.evaluate('[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src)')
            print(name,'scrollWidth',ov,'broken',broken)
            await pg.screenshot(path=name,full_page=full); await c.close()
        await b.close()
asyncio.run(main())

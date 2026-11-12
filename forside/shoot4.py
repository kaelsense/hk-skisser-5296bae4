import asyncio,shutil,glob,subprocess
from playwright.async_api import async_playwright
U='file:///workspace/heikampen/redesign/forside/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        c=await b.new_context(viewport={'width':1440,'height':900}); pg=await c.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='meny-desktop-lukket.png'); await pg.screenshot(path='forside-desktop-topp.png')
        await pg.click('.menu-btn'); await pg.wait_for_timeout(1300)
        await pg.mouse.move(1300,880)
        await pg.screenshot(path='meny-desktop-apen.png')
        await pg.hover('a.mm-main[data-img="2"]'); await pg.wait_for_timeout(900); await pg.screenshot(path='/tmp/hover-kart.png')
        await pg.hover('a.mm-main[data-img="1"]'); await pg.wait_for_timeout(900); await pg.screenshot(path='/tmp/hover-bok.png')
        st=await pg.evaluate("({exp:document.querySelector('.menu-btn').getAttribute('aria-expanded'),lock:getComputedStyle(document.body).overflow,bottom:document.getElementById('megameny').getBoundingClientRect().bottom})")
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
        st2=await pg.evaluate("({exp:document.querySelector('.menu-btn').getAttribute('aria-expanded'),focus:document.activeElement.className})")
        print(st,st2,errs)
        await c.close()
        # ekte hastighet
        c=await b.new_context(viewport={'width':1440,'height':900},record_video_dir='/tmp/vid2',record_video_size={'width':1440,'height':900}); pg=await c.new_page()
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(1000)
        await pg.mouse.move(1380,63,steps=8); await pg.wait_for_timeout(300)
        await pg.click('.menu-btn'); await pg.wait_for_timeout(1200)
        for i in [1,2,3,4]:
            box=await pg.locator(f'a.mm-main[data-img="{i}"]').bounding_box()
            await pg.mouse.move(box['x']+120,box['y']+box['height']/2,steps=12); await pg.wait_for_timeout(900)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(1000)
        vp=await pg.video.path(); await c.close()
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',vp,'-vf','format=yuv420p','-c:v','libx264','-crf','22','-movflags','+faststart','meny-animasjon.mp4'],check=True)
        # mobil
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True); pg=await c.new_page()
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        await pg.tap('.menu-btn'); await pg.wait_for_timeout(1300)
        await pg.evaluate('document.activeElement.blur()'); await pg.wait_for_timeout(500)
        await pg.screenshot(path='meny-mobil-apen.png')
        await pg.evaluate("document.getElementById('megameny').scrollTo(0,9999)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path='/tmp/mob-bottom.png')
        print('sw',await pg.evaluate('document.documentElement.scrollWidth'))
        await c.close(); await b.close()
asyncio.run(main())

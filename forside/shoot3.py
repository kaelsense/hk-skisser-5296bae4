import asyncio
from playwright.async_api import async_playwright
U='file:///workspace/heikampen/redesign/forside/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        c=await b.new_context(viewport={'width':1440,'height':900}); pg=await c.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='meny-desktop-lukket.png'); await pg.screenshot(path='forside-desktop-topp.png')
        await pg.click('.menu-btn')
        for k,t in enumerate([60,140,240,700]):
            await pg.wait_for_timeout(t - ([0,60,140,240][k]))
            await pg.screenshot(path=f'meny-frame-{k+1}.png')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path='meny-desktop-apen.png')
        st=await pg.evaluate("({exp:document.querySelector('.menu-btn').getAttribute('aria-expanded'),focus:document.activeElement.id,lock:getComputedStyle(document.body).overflow})")
        # tab trap: shift+tab from input -> should go to button
        await pg.keyboard.press('Shift+Tab'); a1=await pg.evaluate('document.activeElement.className')
        await pg.keyboard.press('Shift+Tab'); a2=await pg.evaluate('document.activeElement.textContent.trim().slice(0,30)')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
        st2=await pg.evaluate("({exp:document.querySelector('.menu-btn').getAttribute('aria-expanded'),focus:document.activeElement.className,lock:getComputedStyle(document.body).overflow})")
        await pg.click('.menu-btn'); await pg.wait_for_timeout(600); bb=await pg.evaluate("document.getElementById('megameny').getBoundingClientRect().bottom"); print('panel bottom',bb); await pg.mouse.click(700,min(895,bb+10)) if bb<890 else await pg.evaluate("document.querySelector('.mm-backdrop').click()"); await pg.wait_for_timeout(500)
        st3=await pg.evaluate("document.documentElement.classList.contains('menu-open')")
        print('open',st,'trap',a1,'|',a2,'after esc',st2,'outside-click open?',st3,'errs',errs)
        await c.close()
        # video: sakk ned animasjonene 10x via CDP og ta bilder jevnt
        import shutil,os,subprocess
        shutil.rmtree('/tmp/fr',ignore_errors=True); os.makedirs('/tmp/fr')
        c=await b.new_context(viewport={'width':1440,'height':900}); pg=await c.new_page()
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        cdp=await c.new_cdp_session(pg); await cdp.send('Animation.enable'); await cdp.send('Animation.setPlaybackRate',{'playbackRate':0.1})
        n=0
        async def grab(k):
            nonlocal n
            for _ in range(k):
                await pg.screenshot(path=f'/tmp/fr/f{n:04d}.png',scale='css'); n+=1
        await grab(8)
        t0=n
        await pg.evaluate("window.__menu.setOpen(true,{focus:false})")
        await grab(70)
        await pg.evaluate("window.__menu.setOpen(false,{focus:false})")
        await grab(50)
        await c.close()
        print('frames',n)
        # rammer til mp4: hvert bilde ~ (reell tid/10); anslå fps fra målt tid
        subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','24','-i','/tmp/fr/f%04d.png','-vf','scale=1440:-2,format=yuv420p','-c:v','libx264','-crf','22','meny-animasjon.mp4'],check=True)
        for k,idx in enumerate([t0+2,t0+6,t0+12,t0+40]):
            shutil.copy(f'/tmp/fr/f{idx:04d}.png',f'meny-frame-{k+1}.png')
        # mobile
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True); pg=await c.new_page()
        await pg.goto(U,wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='/tmp/mob-closed.png')
        await pg.tap('.menu-btn'); await pg.wait_for_timeout(700)
        await pg.tap('.mm-col--boker .mm-toggle'); await pg.wait_for_timeout(700)
        await pg.screenshot(path='meny-mobil-apen.png')
        print('mobile sw',await pg.evaluate('document.documentElement.scrollWidth'), await pg.evaluate("document.querySelector('.mm-col--boker .mm-toggle').getAttribute('aria-expanded')"))
        await c.close(); await b.close()
asyncio.run(main())

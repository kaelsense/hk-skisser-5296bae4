import asyncio
from playwright.async_api import async_playwright
CSS="#CybotCookiebotDialog,#CybotCookiebotDialogBodyUnderlay,[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=cmplz]{display:none!important} body{overflow:auto!important}"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for name,url in [('nasjonalmuseet','https://www.nasjonalmuseet.no/'),('harvest','https://www.harvestmagazine.no/'),('heikampen','https://heikampen.no/')]:
          for vw,vh,suf in [(1440,900,'d'),(390,844,'m')]:
            ctx=await b.new_context(viewport={'width':vw,'height':vh},is_mobile=(suf=='m'),has_touch=(suf=='m')); pg=await ctx.new_page()
            try: await pg.goto(url,wait_until='networkidle',timeout=40000)
            except Exception as e: print(name,str(e)[:80])
            await pg.add_style_tag(content=CSS); await pg.wait_for_timeout(1500)
            # scroll to trigger lazy
            for y in range(0,6000,800):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(250)
            await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(800)
            try: await pg.screenshot(path=f'{name}-{suf}-full.png',full_page=True,timeout=30000)
            except Exception as e: print(name,suf,str(e)[:100])
            await ctx.close()
        await b.close()
asyncio.run(main())

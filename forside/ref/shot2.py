import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for name,url in [('heikampen','https://heikampen.no/'),('harvest','https://www.harvestmagazine.no/'),('nasjonalmuseet','https://www.nasjonalmuseet.no/')]:
          for vw,vh,suf in [(1440,900,'d'),(390,844,'m')]:
            ctx=await b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=1,is_mobile=(suf=='m'),has_touch=(suf=='m')); pg=await ctx.new_page()
            try: await pg.goto(url,wait_until='networkidle',timeout=40000)
            except Exception as e: print(name,e)
            await pg.wait_for_timeout(1500)
            for t in ['Avvis','AVVIS','Avvis alle','AVVIS ALLE','Godta alle']:
                try:
                    await pg.get_by_role('button',name=t).first.click(timeout=1500); break
                except Exception: pass
            await pg.wait_for_timeout(1000)
            for k,(y) in enumerate([0,900]):
              try:
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(800)
                await pg.screenshot(path=f'{name}-{suf}{k}.png',timeout=15000)
              except Exception as e: print(name,suf,k,str(e)[:100])
            await ctx.close()
        await b.close()
asyncio.run(main())

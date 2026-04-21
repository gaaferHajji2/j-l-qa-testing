import asyncio
from playwright.async_api import async_playwright, expect

async def drag():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        page = await browser.new_page()
        await page.goto("https://www.testmuai.com/selenium-playground/drag-and-drop-demo/")
        t1 = page.get_by_text("Draggable 1", exact=True)
        t2 = page.locator("#mydropzone")
        await t1.hover()
        await page.mouse.down()
        await t2.hover()
        await page.mouse.up()

        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(drag())
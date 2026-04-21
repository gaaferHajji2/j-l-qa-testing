import asyncio
from playwright.async_api import async_playwright, expect, ViewportSize

async def test_01():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        page = await browser.new_page()
        await page.set_viewport_size(viewport_size=ViewportSize({"width": 1024, "height": 1024}))
        await page.goto("https://www.testmuai.com/selenium-playground/radiobutton-demo/")
        t1 = page.get_by_label("Male").nth(0)
        await t1.click()
        await expect(t1).to_be_checked()

        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_01())
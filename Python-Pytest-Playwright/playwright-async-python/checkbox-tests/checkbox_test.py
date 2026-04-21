import asyncio
from playwright.async_api import async_playwright, expect

async def check():
    async with async_playwright() as p:
        chrome = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await chrome.new_page()
        await page.goto("https://www.testmuai.com/selenium-playground/checkbox-demo/")
        t1 = page.get_by_label("Click on check box")
        await expect(t1).not_to_be_checked()
        await t1.click()
        await expect(t1).to_be_checked()
        
if __name__ == '__main__':
    asyncio.run(check())
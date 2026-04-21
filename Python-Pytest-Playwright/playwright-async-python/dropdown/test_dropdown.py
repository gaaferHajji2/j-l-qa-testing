import asyncio
from playwright.async_api import async_playwright, expect

async def single_dropdown():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2500)
        page = await browser.new_page()
        await page.goto("https://www.testmuai.com/selenium-playground/select-dropdown-demo/")
        t1 = page.locator("#select-demo")
        await t1.click()
        await t1.select_option("Sunday")
        await expect(t1).to_have_value("Sunday")
        await t1.click()
        await t1.select_option(index=3)
        await expect(t1).to_have_value("Tuesday")
        await t1.click()
        await t1.select_option(value="Thursday")
        await expect(t1).to_have_value("Thursday")

        await page.close()
        await browser.close()

async def multi_dropdown():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2500)
        page = await browser.new_page()
        await page.goto("https://www.testmuai.com/selenium-playground/select-dropdown-demo/")
        t1 = page.locator("#multi-select")
        await t1.scroll_into_view_if_needed()
        await t1.select_option(["New York", "Ohio", "Florida"])
        await expect(t1).to_have_values(['Florida', 'New York', 'Ohio'])

        await page.close()
        await browser.close()

if __name__ == '__main__':
    # asyncio.run(single_dropdown())
    asyncio.run(multi_dropdown())
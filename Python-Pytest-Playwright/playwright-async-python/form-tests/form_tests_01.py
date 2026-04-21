import asyncio
from playwright.async_api import async_playwright, expect

async def test_go_to():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto('https://www.testmu.ai/selenium-playground/simple-form-demo/')
        await expect(page).to_have_title("Selenium Grid Online | Run Selenium Test On Cloud")

        msg01 = "JLoka-01"
        await page.wait_for_timeout(5000)
        t1 = page.get_by_placeholder("Please enter your Message")
        await t1.type(msg01)
        t2 = page.get_by_role('button', name='Get Checked Value')
        await t2.hover()
        await t2.click()
        # await t1.type(msg01)
        # await t2.click()
        t3 = page.locator('#message')
        await expect(t3).to_have_text(msg01)

        await page.close()
        await browser.close()

async def test_sum():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1500)
        page = await browser.new_page()
        await page.goto('https://www.testmu.ai/selenium-playground/simple-form-demo/')
        t1 = page.get_by_placeholder('Please enter first value')
        t2 = page.get_by_placeholder('Please enter second value')
        t3 = page.get_by_role('button', name='Get Sum')
        t4 = page.locator('#addmessage')
        await t3.scroll_into_view_if_needed()
        await t1.fill('1')
        await t2.fill('2')
        await t3.click()
        await expect(t4).to_have_text('3')

        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_go_to())
    asyncio.run(test_sum())
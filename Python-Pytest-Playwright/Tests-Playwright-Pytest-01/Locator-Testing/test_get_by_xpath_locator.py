from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto('https://bootswatch.com/flatly/')
    t1 = page.locator('xpath=(//button[text()="Primary"])[1]')
    t1.scroll_into_view_if_needed()
    t1.highlight()
    time.sleep(1)

    t2 = page.locator('xpath=(//button[text()="Primary"])').nth(2)
    t2.scroll_into_view_if_needed()
    t2.highlight()
    time.sleep(2)

    page.close()
    browser.close()
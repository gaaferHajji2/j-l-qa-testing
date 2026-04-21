from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto('https://bootswatch.com/flatly/')
    xpath_locator = "//a[@id='themes']"
    t1 = page.locator(f"xpath={xpath_locator}")
    t1.click()
    # In milli-seconds
    t1.dblclick(delay=1000)
    t1.click()
    # click the right button of mouse
    # t1.click(button='right')

    t2 = page.locator("css=button.btn.btn-outline-primary")
    t2.scroll_into_view_if_needed()
    t2.hover()

    time.sleep(2)
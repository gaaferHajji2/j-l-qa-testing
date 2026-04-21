from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto('https://bootswatch.com/flatly/')
    t1 = page.get_by_placeholder("Enter email")
    t1.scroll_into_view_if_needed()
    # t1.fill("test@test.com")
    # Delay in milliseconds
    t1.type("test@test.com", delay=100)

    time.sleep(2)
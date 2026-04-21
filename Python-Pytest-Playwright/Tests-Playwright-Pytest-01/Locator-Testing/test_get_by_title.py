from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://bootswatch.com/default/")
    page.get_by_title("attribute").scroll_into_view_if_needed()
    page.get_by_title("attribute").highlight()

    page.get_by_title("Source Title").first.scroll_into_view_if_needed()
    page.get_by_title("Source Title").first.highlight()

    time.sleep(2)
    page.close()
    browser.close()
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()

    page.goto("https://www.pexels.com/")
    page.get_by_alt_text("Nature in Motion Challenge").highlight()
    time.sleep(3)
    page.close()
    browser.close()
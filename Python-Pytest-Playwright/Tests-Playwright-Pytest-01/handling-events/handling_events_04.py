from playwright.sync_api import sync_playwright

def on_load(page):
    print(f"The Page Loaded Successfully: {page}")

def on_request(request):
    print(f"The Request is: {request}")
    print(f"The request class is: {request.__class__}")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.on("load", on_load)
    page.on("request", on_request)
    page.goto("https://www.scrapethissite.com/pages/ajax-javascript")
    
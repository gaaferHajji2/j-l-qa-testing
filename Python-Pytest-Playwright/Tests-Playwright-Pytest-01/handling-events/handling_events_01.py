from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1500)
    page = browser.new_page()
    page.goto("https://bootswatch.com/")

    themes_btn = page.locator("#themes")
    themes_btn.click()

    default_theme = page.locator('.dropdown-item').nth(0)
    default_theme.click()
    print(f"The page URL is: {page.url}")
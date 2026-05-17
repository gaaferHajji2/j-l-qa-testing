from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/ajax-javascript/")
    link = page.get_by_role("link", name="2015")
    link.click()
    table = page.wait_for_selector(".table")
    print(f"The table is: {table}")
    titles = table.query_selector_all(".film-title")

    for title in titles:
        print(f"The title is: {title.inner_html()}")
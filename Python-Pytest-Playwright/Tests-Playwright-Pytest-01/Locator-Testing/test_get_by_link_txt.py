from playwright.sync_api import sync_playwright

# Same as: playwright = sync_playwright().start()
with sync_playwright() as playwright: # This Is For Starting sync playwright Using with-context
    
    # This Will Start Chromium Browser With Headless-Option AS False
    # And The Slow Mode Will Increase x1000
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    # This Will Create New Page Using The Browser
    page = browser.new_page()
    # This Will Change The Browser URL
    page.goto("https://playwright.dev/python")

    # This Will Return The Links With Text=Docs
    docs_links = page.get_by_role('link', name='Docs')
    # This Will Highlight The Main Object
    docs_links.highlight()
    # The Page-Object.url Will Return The Current URL
    print("The Current URL Is: ", page.url)
    # This Will Fire The Click-Event
    docs_links.click()
    print("The Current URL Is: ", page.url)

    # This Will Close The Page
    page.close()
    # This Will Close The Browser
    browser.close()
    # Here AS We Use with-Keyword, Then stop()-Method Will Call Automatically
    # playwright.stop()
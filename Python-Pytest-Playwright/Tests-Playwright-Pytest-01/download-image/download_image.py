from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(slow_mo=500, headless=False)
    page = browser.new_page()
    page.goto("https://unsplash.com/photos/pizza-with-berries-MQUqbmszGGM")
    download_btn = page.get_by_role('link', name="Download free")
    with page.expect_download() as download_info:
        download_btn.click()
    download_file = download_info.value
    download_file.save_as("./pizza.jpg")
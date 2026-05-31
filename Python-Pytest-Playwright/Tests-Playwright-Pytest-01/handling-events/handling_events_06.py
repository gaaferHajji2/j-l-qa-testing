from playwright.sync_api import sync_playwright, Download

def on_download(download: Download):
    print(f"The download is: {download}")
    download.save_as("./pizza.jpg")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(slow_mo=500, headless=False)
    page = browser.new_page()
    page.goto("https://unsplash.com/photos/pizza-with-berries-MQUqbmszGGM")
    page.on("download", on_download)
    download_btn = page.get_by_role('link', name="Download free")
    with page.expect_download() as download_info:
        download_btn.click()
    page.close()
    browser.close()
from playwright.sync_api import sync_playwright

with sync_playwright() as playwrite:
    chrome = playwrite.chromium.launch(headless=False, slow_mo=1500)
    page = chrome.new_page()
    page.goto("https://bootswatch.com/cosmo/")
    upload_file_item = page.get_by_label("Default file input example")
    upload_file_item.scroll_into_view_if_needed()
    # Here we can upload multiple files
    upload_file_item.set_input_files("test.txt")

    page.close()
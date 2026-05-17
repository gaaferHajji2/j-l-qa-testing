from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1500)
    page = browser.new_page()

    page.goto("https://bootswatch.com/cosmo/")
    textarea_element = page.get_by_label("Example textarea")
    textarea_element.scroll_into_view_if_needed()
    textarea_element.click()
    textarea_element.press("Shift+KeyJ")
    textarea_element.press("KeyA")
    textarea_element.press("KeyF")
    textarea_element.press("KeyA")
    textarea_element.press("KeyR")
    textarea_element.press("Space")
    textarea_element.press("Shift+KeyL")
    textarea_element.press("KeyO")
    textarea_element.press("KeyK")
    textarea_element.press("KeyA")

    page.close()
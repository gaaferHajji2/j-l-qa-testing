from playwright.sync_api import sync_playwright

def on_dialog(dialog):
    print("The dialog object is: ", dialog)
    dialog.accept("My Name is Jafar Loka")
    # dialog.dismiss()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(slow_mo=500, headless=False)
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/javascript_alerts")
    
    alert_btn = page.get_by_text("Click for JS Alert")
    alert_btn.click()


    page.on('dialog', on_dialog)
    confirm_btn = page.get_by_text("Click for JS Confirm")
    confirm_btn.click()

    prompt_btn = page.get_by_text("Click for JS Prompt")
    prompt_btn.click()

    page.close()
    browser.close()
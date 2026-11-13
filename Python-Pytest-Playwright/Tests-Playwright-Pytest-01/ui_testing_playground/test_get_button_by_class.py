from playwright.sync_api import Page, expect

def handle_dialog(dialog):
    assert dialog.type == 'alert'
    assert dialog.message == 'Primary button pressed'
    print('Handling dialog')
    dialog.accept()

def test_click_primary_button(page: Page):
    page.goto('http://www.uitestingplayground.com/classattr')
    page.once('dialog', handle_dialog)

    button = page.locator('button.btn-primary')
    button.click()
    
    expect(button).to_be_visible()
    expect(button).to_be_enabled()
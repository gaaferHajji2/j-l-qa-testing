from playwright.sync_api import Page, expect

def test_click_button_with_dynamic_id(page: Page):
    page.goto("http://www.uitestingplayground.com/dynamicid")
    button = page.get_by_role('button', name="Button with Dynamic ID")
    button.click()
    expect(button).to_be_visible()
    expect(button).to_be_enabled()

from playwright.sync_api import expect, Page

def test_orange_hrm_title(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    username = page.get_by_placeholder("Username")
    username.fill("Admin")
    password = page.get_by_placeholder("Password")
    password.fill("admin123")
    expect(username).to_be_visible()
    expect(password).to_be_editable()
    page.get_by_role("button", name="Login").click()

    
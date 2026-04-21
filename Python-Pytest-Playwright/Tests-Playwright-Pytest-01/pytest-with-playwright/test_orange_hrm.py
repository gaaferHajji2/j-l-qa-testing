from playwright.sync_api import Page

def test_orange_hrm_title(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    username = page.get_by_placeholder("Username")
    username.fill("Admin")
    password = page.get_by_placeholder("Password")
    password.fill("admin123")
    page.get_by_role("button", name="Login").click()
    assert page.url == "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
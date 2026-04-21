from playwright.sync_api import Browser
import time

def test_orange_hrm_title(browser: Browser):
    context = browser.new_context(
        record_video_dir="."
    )
    page = context.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    username = page.get_by_placeholder("Username")
    username.fill("Admin")
    # username.screenshot(path="username.png")
    password = page.get_by_placeholder("Password")
    password.fill("admin123")
    # password.screenshot(path="password.png")
    page.get_by_role("button", name="Login").click()
    page.wait_for_selector("css=canvas[height='265']", state='attached')
    time.sleep(2)
    # page.screenshot(path="test.png", full_page=True)
    assert page.url == "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
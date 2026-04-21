from playwright.sync_api import BrowserContext, Page
import pytest
import time

@pytest.fixture(autouse=True)
def trace_test(context: BrowserContext):
    
    # enable saving snapshots of our test for every action
    context.tracing.start(
        name="hrm_trace", 
        screenshots=True, 
        # snapshots: save real state of page that we can handle it using the viewer
        snapshots=True, # enable screenshot of tracing frame by frame
        sources=True # enable saving snapshots of our test for every action
    )
    yield
    context.tracing.stop(path="trace.zip")

def test_orange_hrm_title(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    username = page.get_by_placeholder("Username")
    username.fill("Admin")
    username.screenshot(path="username.png")
    password = page.get_by_placeholder("Password")
    password.fill("admin123")
    page.get_by_role("button", name="Login").click()
    page.wait_for_selector("css=canvas[height='265']", state='attached')
    time.sleep(2)
    assert page.url == "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
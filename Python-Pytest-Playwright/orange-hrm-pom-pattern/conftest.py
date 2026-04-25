from datetime import datetime
import pytest
from playwright.async_api import Browser
from utils.logger import logger

# Hook to attach test outcome for screenshot fixture
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    logger.info("Running pytest_runtest_makereport")
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    return rep

# @pytest.fixture(scope="session")
# async def browser():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False, slow_mo=500)  # slow_mo for visibility in headed mode
#         logger.info("Browser launched (Chromium)")
#         yield browser
#         await browser.close()
#         logger.info("Browser closed")

@pytest.fixture(scope="function")
async def page(browser: Browser):
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        # record_video_dir="videos/"  # optional video recording
    )
    page = await context.new_page()
    logger.info("New page created")
    yield page

    # Screenshot on failure
    if hasattr(page, "rep_call") and page.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/FAIL_{page.rep_call.nodeid.replace('::', '_')}_{timestamp}.png"
        await page.screenshot(path=screenshot_path)
        logger.error(f"TEST FAILED - Screenshot saved: {screenshot_path}")

    await context.close()
    logger.info("Page context closed")

# Optional: Logged-in page fixture (reused across tests)
@pytest.fixture
async def logged_in_page(page):
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    await login_page.navigate_to_login()
    await login_page.login("Admin", "Admin123")  # Credentials as provided
    logger.info("✅ Logged in as Admin")
    yield page
    # Optional cleanup: logout can be called in individual tests if needed

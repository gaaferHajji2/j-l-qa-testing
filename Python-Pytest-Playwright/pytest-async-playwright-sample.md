**Senior QA Automation Framework: OrangeHRM Demo Tests (Python + Async Playwright + Pytest + POM)**

This is a complete, production-grade setup following senior QA best practices:
- **Async Playwright** for fast, reliable browser automation.
- **Pytest** with `pytest-asyncio` for clean async test execution.
- **Page Object Model (POM)** for maintainability and reusability.
- **Logging** of every step (console + file).
- **Automatic screenshots** on test failure (plus manual screenshots where required).
- **Robust, accessible locators** (prefer `get_by_placeholder`, `get_by_role`, `get_by_text`, XPath where needed).
- **Fixtures** for browser/page management and logged-in state.
- **Clear folder structure** and configuration files.

### 1. Folder Structure
```
orangehrm_tests/
├── conftest.py                 # Fixtures, hooks, browser setup, screenshots on failure
├── pytest.ini                  # Pytest configuration
├── requirements.txt
├── utils/
│   └── logger.py               # Centralized logging
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Base class with common methods
│   ├── login_page.py
│   └── dashboard_page.py       # Reusable for all post-login actions
├── tests/
│   ├── __init__.py
│   └── test_orangehrm.py       # 5+ simple tests (expandable)
├── logs/                       # Auto-created test logs
└── screenshots/                # Auto-created failure + required screenshots
```

### 2. Necessary Steps to Run the Tests
1. Create the folder structure above.
2. `cd orangehrm_tests`
3. Create virtual environment: `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows).
4. Install dependencies: `pip install -r requirements.txt`
5. Install Playwright browsers: `playwright install chromium`
6. Create empty folders: `mkdir -p logs screenshots`
7. Run tests:  
   ```bash
   pytest -v --headed --browser chromium   # Headed mode for debugging
   # OR headless: pytest -v
   # Run specific test: pytest -v -k "successful_login"
   ```
8. Logs → `logs/test.log`  
   Screenshots → `screenshots/` (named by test + timestamp on failure)

### 3. File Contents

#### `requirements.txt`
```txt
pytest>=8.3.0
pytest-asyncio>=0.25.0
playwright>=1.48.0
```

#### `pytest.ini`
```ini
[pytest]
asyncio_mode = auto
python_files = test_*.py
addopts = -v --tb=short --maxfail=3
log_cli = true
log_cli_level = INFO
```

#### `utils/logger.py`
```python
import logging
import sys
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("orangehrm_qa")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # File handler
    log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()
```

#### `conftest.py`
```python
import pytest
import asyncio
from playwright.async_api import async_playwright, Page
from utils.logger import logger
from datetime import datetime

# Hook to attach test outcome for screenshot fixture
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
    return rep

@pytest.fixture(scope="session")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)  # slow_mo for visibility in headed mode
        logger.info("Browser launched (Chromium)")
        yield browser
        await browser.close()
        logger.info("Browser closed")

@pytest.fixture(scope="function")
async def page(browser):
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir="videos/"  # optional video recording
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
```

#### `pages/base_page.py`
```python
from playwright.async_api import Page
from utils.logger import logger
from datetime import datetime

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate_to(self, url: str):
        await self.page.goto(url, wait_until="networkidle")
        logger.info(f"Navigated to: {url}")

    async def take_screenshot(self, name: str):
        """Manual screenshot for key verification steps"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"
        await self.page.screenshot(path=path)
        logger.info(f"Screenshot captured: {path}")
```

#### `pages/login_page.py`
```python
from pages.base_page import BasePage
from utils.logger import logger
from playwright.async_api import expect

class LoginPage(BasePage):
    async def navigate_to_login(self):
        await self.navigate_to("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    async def login(self, username: str, password: str):
        logger.info(f"Step 1: Entering username '{username}'")
        await self.page.get_by_placeholder("Username").fill(username)

        logger.info("Step 2: Entering password")
        await self.page.get_by_placeholder("Password").fill(password)

        logger.info("Step 3: Clicking Login button")
        await self.page.locator("button[type='submit']").click()

        # Wait for navigation
        await self.page.wait_for_url("**/dashboard/index", timeout=10000)
        logger.info("✅ Login successful - redirected to Dashboard")

    async def get_error_message(self):
        error = self.page.get_by_text("Invalid credentials")
        await expect(error).to_be_visible(timeout=5000)
        text = await error.inner_text()
        logger.info(f"Error message displayed: {text}")
        return text
```

#### `pages/dashboard_page.py`
```python
from pages.base_page import BasePage
from utils.logger import logger
from playwright.async_api import expect

class DashboardPage(BasePage):
    async def verify_dashboard_loaded(self):
        logger.info("Step: Verifying Dashboard page")
        header = self.page.get_by_role("heading", name="Dashboard")
        await expect(header).to_be_visible(timeout=10000)
        await self.take_screenshot("dashboard_loaded")  # Required screenshot
        logger.info("✅ Dashboard loaded successfully")

    async def navigate_to_admin(self):
        logger.info("Step: Clicking Admin menu")
        await self.page.locator("//span[normalize-space()='Admin']").click()
        await self.page.wait_for_url("**/admin/viewSystemUsers", timeout=10000)
        await expect(self.page.get_by_role("heading", name="Admin")).to_be_visible()
        await self.take_screenshot("admin_page")
        logger.info("✅ Navigated to Admin module")

    async def navigate_to_pim(self):
        logger.info("Step: Clicking PIM menu")
        await self.page.locator("//span[normalize-space()='PIM']").click()
        await self.page.wait_for_url("**/pim/viewEmployeeList", timeout=10000)
        await expect(self.page.get_by_role("heading", name="Employee Information")).to_be_visible()
        await self.take_screenshot("pim_page")
        logger.info("✅ Navigated to PIM (Employee List)")

    async def logout(self):
        logger.info("Step: Opening user dropdown")
        await self.page.locator(".oxd-userdropdown-name").click()
        logger.info("Step: Clicking Logout")
        await self.page.get_by_text("Logout").click()
        await self.page.wait_for_url("**/auth/login", timeout=10000)
        logger.info("✅ Logout successful")
```

#### `tests/test_orangehrm.py` (5+ Simple Tests)
```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger

@pytest.mark.asyncio
async def test_successful_login_and_verify_dashboard(page):
    """Test 1: Valid login + Dashboard verification"""
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    await login_page.navigate_to_login()
    await login_page.login("Admin", "Admin123")
    await dashboard_page.verify_dashboard_loaded()
    logger.info("✅ Test 1 PASSED")

@pytest.mark.asyncio
async def test_invalid_login_shows_error(page):
    """Test 2: Invalid credentials error"""
    login_page = LoginPage(page)
    await login_page.navigate_to_login()
    await login_page.login("Admin", "WrongPass123")
    error = await login_page.get_error_message()
    assert "Invalid credentials" in error
    await login_page.take_screenshot("invalid_login_error")  # Required screenshot
    logger.info("✅ Test 2 PASSED")

@pytest.mark.asyncio
async def test_navigate_to_admin_module(logged_in_page):
    """Test 3: Navigate to Admin module (uses logged-in fixture)"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.navigate_to_admin()
    logger.info("✅ Test 3 PASSED")

@pytest.mark.asyncio
async def test_navigate_to_pim_module(logged_in_page):
    """Test 4: Navigate to PIM (Employee List)"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.navigate_to_pim()
    logger.info("✅ Test 4 PASSED")

@pytest.mark.asyncio
async def test_logout_functionality(logged_in_page):
    """Test 5: Full logout flow"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.logout()
    # Verify back on login page
    await expect(logged_in_page.get_by_placeholder("Username")).to_be_visible()
    await dashboard_page.take_screenshot("after_logout")
    logger.info("✅ Test 5 PASSED")
```

### Summary
- **5 complete tests** (easily extensible).
- Every critical step is logged.
- Screenshots are taken automatically on failure + manually for key verification points.
- POM keeps code clean and maintainable.
- Fully async, senior-level configuration with fixtures and hooks.

Run the tests and you will get detailed logs + screenshots for every failure (or required step). This framework is ready for CI/CD integration (GitHub Actions, Jenkins, etc.). Let me know if you need more tests, API tests, or CI pipeline!
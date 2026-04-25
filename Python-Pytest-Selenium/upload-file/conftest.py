import pytest
from utils.logger import setup_logger
from config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

logger = setup_logger(__name__)

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Setup test environment before all tests"""
    Config.setup_dirs()
    logger.info("Test environment initialized")
    yield
    logger.info("Test environment cleaned up")

@pytest.fixture()
def driver(request):
    """
    Pytest fixture for WebDriver instance
    Provides browser setup/teardown with failure screenshot capture
    """
    browser = Config.BROWSER.lower()
    logger.info(f"Initializing {browser} driver...")
    
    if browser == "chrome":
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        
    elif browser == "firefox":
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Configure driver
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.maximize_window()
    
    yield driver
    
    # Teardown: Capture screenshot on failure
    if request.node.rep_call.failed:
        test_name = request.node.name
        logger.error(f"Test failed: {test_name}")
        # Note: screenshot capture handled in test via page object
    
    driver.quit()
    logger.info("Browser driver closed")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test outcome for screenshot logic
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

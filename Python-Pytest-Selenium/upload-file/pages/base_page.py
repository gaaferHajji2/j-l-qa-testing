from abc import ABC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from utils.logger import setup_logger
from utils.screenshot import capture_screenshot

logger = setup_logger(__name__)

class BasePage(ABC):
    """
    Base class for all Page Objects
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.base_url = Config.BASE_URL
    
    def open(self, url: str = None):
        """Navigate to URL"""
        target_url = url or self.base_url
        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self
    
    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_clickable(self, locator):
        """Find clickable element with explicit wait"""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise
    
    def capture_failure_screenshot(self, test_name: str):
        """Capture screenshot on test failure"""
        path = capture_screenshot(
            self.driver, 
            test_name, 
            Config.SCREENSHOTS_DIR
        )
        if path:
            logger.warning(f"Screenshot saved: {path}")
        return path
    
    def scroll_into_view(self, element):
        """Scroll element into viewport"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self

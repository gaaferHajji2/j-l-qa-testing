from datetime import datetime
from pathlib import Path
import logging
from selenium.webdriver.remote.webdriver import WebDriver

def capture_screenshot(driver: WebDriver, test_name: str, output_dir: Path) -> str:
    """
    Capture screenshot and save with timestamp
    Returns: Path to saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_failure_{timestamp}.png"
    filepath = output_dir / filename
    
    try:
        driver.save_screenshot(str(filepath))
        return str(filepath)
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")
        return None

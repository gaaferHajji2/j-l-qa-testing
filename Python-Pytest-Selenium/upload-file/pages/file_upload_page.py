from selenium.webdriver.common.by import By
from utils.logger import setup_logger
from pages.base_page import BasePage

logger = setup_logger(__name__)

class FileUploadPage(BasePage):
    """
    Page Object representing a page with file upload capability
    """
    
    # Locators - UPDATE THESE for your actual target site
    FILE_INPUT_LOCATOR = (By.CSS_SELECTOR, "input[type='file']")
    UPLOAD_BUTTON_LOCATOR = (By.ID, "upload-btn")  # Example
    UPLOAD_STATUS_LOCATOR = (By.ID, "upload-status")  # Example
    
    def __init__(self, driver):
        super().__init__(driver)
        self.file_input = None
    
    def open(self):
        """Override to navigate to target page"""
        return super().open()
    
    def is_file_input_present(self) -> bool:
        """Check if file input element exists on page"""
        try:
            self.file_input = self.find_element(self.FILE_INPUT_LOCATOR)
            logger.info("File input element found")
            return True
        except Exception:
            logger.warning("File input element NOT found - page may not support uploads")
            return False
    
    def open_file_chooser_dialog(self):
        """
        CASE 1: Trigger the native file chooser dialog
        Note: This opens the OS dialog but cannot be automated further
        due to browser security restrictions.
        """
        logger.info("Attempting to open file chooser dialog...")
        if not self.file_input:
            self.file_input = self.find_element(self.FILE_INPUT_LOCATOR)
        
        # Clicking opens OS dialog (cannot be controlled via Selenium)
        self.file_input.click()
        logger.warning("⚠️  Native file dialog opened - manual interaction required")
        logger.warning("⚠️  Selenium cannot automate OS-level dialogs")
        return self
    
    def send_file_directly(self, file_path: str):
        """
        CASE 2: Send file path directly to input element
        This is the RECOMMENDED approach for Selenium automation
        """
        logger.info(f"Sending file directly: {file_path}")
        
        if not self.file_input:
            self.file_input = self.find_element(self.FILE_INPUT_LOCATOR)
        
        # Send absolute path to bypass dialog
        self.file_input.send_keys(file_path)
        logger.info(f"File path sent to input: {file_path}")
        return self
    
    def click_upload_button(self):
        """Click the upload/submit button if present"""
        try:
            upload_btn = self.find_clickable(self.UPLOAD_BUTTON_LOCATOR)
            upload_btn.click()
            logger.info("Upload button clicked")
        except Exception as e:
            logger.warning(f"Upload button not found or not clickable: {e}")
        return self
    
    def get_upload_status(self) -> str:
        """Get upload status message if available"""
        try:
            status_elem = self.find_element(self.UPLOAD_STATUS_LOCATOR)
            return status_elem.text
        except Exception:
            logger.error("Status element not found")
            return "Status element not found"

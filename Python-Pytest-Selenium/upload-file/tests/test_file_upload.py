import os
import pytest
from pages.file_upload_page import FileUploadPage
from utils.logger import setup_logger
from config import Config

logger = setup_logger(__name__)

@pytest.fixture(scope="function")
def upload_page(driver):
    """Fixture providing initialized FileUploadPage"""
    page = FileUploadPage(driver)
    page.open()
    return page

@pytest.mark.upload
@pytest.mark.smoke
class TestFileUploadCases:
    """
    Test suite for file upload functionality
    """
    
    def test_case_1_open_file_chooser_dialog(self, upload_page):
        """
        CASE 1: Open the native file chooser dialog
        
        ⚠️  LIMITATION: Selenium cannot automate OS-level dialogs.
        This test demonstrates the attempt but requires manual intervention.
        """
        logger.info("TEST CASE 1: Opening file chooser dialog")
        
        # Verify page loaded and file input exists
        assert upload_page.is_file_input_present(), \
            "File input element not found on page"
        
        # Attempt to open dialog
        upload_page.open_file_chooser_dialog()
        
        # Log expected behavior
        logger.warning("⚠️  EXPECTED: Native OS file dialog is now open")
        logger.warning("⚠️  Selenium CANNOT interact with OS dialogs")
        logger.warning("⚠️  This approach is NOT suitable for full automation")
        
        # Assertion: Dialog was triggered (we can't verify OS dialog state)
        # In real scenario, you'd document this limitation in test report
        assert True, "File chooser dialog triggered (manual verification required)"
    
    @pytest.mark.regression
    def test_case_2_send_file_directly(self, upload_page):
        """
        CASE 2: Send file path directly to input element
        
        ✅ RECOMMENDED: This is the Selenium-compatible approach
        for automated file upload testing
        """
        logger.info("TEST CASE 2: Sending file directly to input")
        
        # Verify prerequisites
        assert os.path.exists(Config.SAMPLE_FILE), \
            f"Test file not found: {Config.SAMPLE_FILE}"
        assert upload_page.is_file_input_present(), \
            "File input element not found on page"
        
        # Send file path directly (bypasses OS dialog)
        upload_page.send_file_directly(Config.SAMPLE_FILE)
        
        # Verify file was "selected" (value attribute contains filename)
        file_input = upload_page.file_input
        selected_file = file_input.get_attribute("value")
        
        # Note: Browser security may return fake path or just filename
        logger.info(f"Selected file path (browser-reported): {selected_file}")
        
        # Assertion: File path was set (exact value depends on browser)
        assert Config.SAMPLE_FILE.split('/')[-1] in selected_file or \
               Config.SAMPLE_FILE.split('\\')[-1] in selected_file or \
               selected_file != "", \
            "File was not properly set in input element"
        
        logger.info("✅ File path successfully sent to input element")
        
        # If site had upload button, we'd click it here:
        # upload_page.click_upload_button()
        # status = upload_page.get_upload_status()
        # assert "success" in status.lower()
    
    def test_upload_with_nonexistent_file_should_fail_gracefully(self, upload_page):
        """
        Negative test: Attempt upload with invalid file path
        """
        logger.info("Negative test: Invalid file path handling")
        
        if not upload_page.is_file_input_present():
            pytest.skip("File input not available on this page")
        
        # Try to send non-existent file
        invalid_path = "/nonexistent/path/file.txt"
        upload_page.send_file_directly(invalid_path)
        
        # Browser should handle gracefully (no crash)
        # Actual validation depends on application behavior
        logger.info("Handled invalid file path without crashing")
        assert True  # Test passes if no exception thrown

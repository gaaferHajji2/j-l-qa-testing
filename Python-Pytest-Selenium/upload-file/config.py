import os
from pathlib import Path

class Config:
    # Base URLs
    BASE_URL = "https://bootswatch.com/cerulean/"
    
    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")  # chrome, firefox, headless
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 30
    
    # File paths
    ROOT_DIR = Path(__file__).parent.parent
    TEST_DATA_DIR = ROOT_DIR / "test_data"
    REPORTS_DIR = ROOT_DIR / "reports"
    SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
    
    # Test file for upload
    SAMPLE_FILE = str(TEST_DATA_DIR / "sample.txt")
    
    # Ensure directories exist
    @classmethod
    def setup_dirs(cls):
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.SCREENSHOTS_DIR.mkdir(exist_ok=True)

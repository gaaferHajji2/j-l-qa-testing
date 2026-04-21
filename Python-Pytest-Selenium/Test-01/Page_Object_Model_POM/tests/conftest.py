from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pytest

@pytest.fixture(scope='session')
def get_driver_and_web_wait():
    base_url = "https://www.letskodeit.com/"
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver=driver, timeout=15, poll_frequency=1.0)
    driver.maximize_window()
    driver.get(base_url)
    yield driver, wait
    time.sleep(1)
    driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

class TestChromeDriver:

    def __init__(self):
        self.ex_path = 'chromedriver.exe'

    def test_01(self):
        service = Service(executable_path=self.ex_path)
        driver = webdriver.Chrome(service=service)
        driver.get("https://letskodeit.com")
        time.sleep(10)

test=TestChromeDriver()
test.test_01()
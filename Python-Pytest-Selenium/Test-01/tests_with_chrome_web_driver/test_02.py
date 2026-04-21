from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestGetElementByIdAndNameAndXPathAndCSSSelectorAndMore:
    def __init__(self):
        self.service = Service(executable_path='chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service)

    def get_page(self):
        self.driver.get("https://www.letskodeit.com/practice")
        self.element = WebDriverWait(driver=self.driver, timeout=15).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="bmwradio"]'))
        )
        #  = self.driver.find_element(By.XPATH, '//input[@id="bmwradio"]')
        self.element_02 = self.driver.find_element(By.ID, 'name')
        self.element_03 = self.driver.find_element(By.NAME, 'show-hide')
        self.element_04 = self.driver.find_element(By.CSS_SELECTOR, '#enabled-button')
        self.element_05 = self.driver.find_element(By.LINK_TEXT, 'ALL COURSES')
        self.element_06 = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'BLOG')
        self.element_07 = self.driver.find_element(By.CLASS_NAME, 'left-align')
        self.element_08 = self.driver.find_element(By.TAG_NAME, 'h1')
        self.element_09 = self.driver.find_elements(By.TAG_NAME, 'a')

        print("The Element Is: ", self.element)
        print("The Element By Id Is: ", self.element_02)
        print("The Element By Name Is: ", self.element_03)
        print("The Element By CSS Selector Is: ", self.element_04)
        print("The Element By LINK TEXT Is: ", self.element_05.text)
        print("The Element By PARTIAL LINK TEXT Is: ", self.element_06.text)
        print("The Element By CLASS NAME Is: ", self.element_07)
        print("The Element By TAG NAME Is: ", self.element_08.text)
        print("The List Of A-Tag Is: ", len(self.element_09))

test= TestGetElementByIdAndNameAndXPathAndCSSSelectorAndMore()

test.get_page()
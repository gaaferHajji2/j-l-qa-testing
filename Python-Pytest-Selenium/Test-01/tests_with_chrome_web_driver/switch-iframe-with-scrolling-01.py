from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.get("https://www.letskodeit.com/practice")
driver.execute_script("window.scrollBy(0, 1000)")
time.sleep(1)
driver.switch_to.frame(driver.find_element(By.ID, 'courses-iframe'))
t1 = driver.find_element(By.XPATH, '//input[@id="search"]')
t1.send_keys("Python")
time.sleep(3)

# driver.switch_to.parent_frame()
driver.switch_to.default_content()
driver.execute_script("window.scrollBy(0, -750)")
time.sleep(3)
driver.quit()
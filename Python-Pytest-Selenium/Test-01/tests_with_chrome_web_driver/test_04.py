from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.letskodeit.com/")
login_element = WebDriverWait(driver=driver, timeout=15).until(
    EC.presence_of_element_located((By.XPATH, '//a[@href="/login"]'))
)
#  driver.find_element(By.XPATH, '//a[@href="/login"]')
print("The Login Element IS: ", login_element)
login_element.click()
print("The Current Page URL Is: ", driver.current_url)
email_input = WebDriverWait(driver=driver, timeout=15).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="email"]'))
)
password_input = driver.find_element(By.XPATH, '//input[@id="login-password"]')
print("The Email Input Is: ", email_input)
print("The Password Input Is: ", password_input)
email_input.send_keys("gaafer@loka.com")
password_input.send_keys("Test@1234567890")
login_btn = driver.find_element(By.XPATH, '//button[@id="login"]')
login_btn.click()
time.sleep(10)
print("The Current Page URL Is: ", driver.current_url)
driver.quit()
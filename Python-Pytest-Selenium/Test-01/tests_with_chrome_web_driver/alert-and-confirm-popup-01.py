from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.letskodeit.com/practice")
t1 = driver.find_element(By.ID, 'name')
t1.send_keys("Jafar Loka")
t2 = driver.find_element(By.ID, 'alertbtn')
t3 = driver.find_element(By.ID, 'confirmbtn')
t2.click()
time.sleep(1)
t4 = driver.switch_to.alert
t4.accept()
time.sleep(3)
t3.click()
t5 = driver.switch_to.alert
time.sleep(1)
t5.dismiss()
time.sleep(1)
driver.quit()
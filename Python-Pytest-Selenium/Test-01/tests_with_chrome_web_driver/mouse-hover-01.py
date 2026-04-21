from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.letskodeit.com/practice")
driver.execute_script("window.scrollBy(0, 700)")

time.sleep(1)
t1 = driver.find_element(By.XPATH, '//div[@class="mouse-hover"]')

try:
    actionChains = ActionChains(driver=driver)
    actionChains.move_to_element(to_element=t1).perform()
    time.sleep(3)
    t2 = driver.find_element(By.XPATH, '//div[@class="mouse-hover"]//a[text()="Top"]')
    t3 = driver.find_element(By.XPATH, '//div[@class="mouse-hover"]//a[text()="Reload"]')
    # t2.click()
    # Second Way
    actionChains.move_to_element(to_element=t2).click().perform()

    time.sleep(3)

except Exception as e:
    print("The Exception Is: ", e.__str__())
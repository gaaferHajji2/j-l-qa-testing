from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://jqueryui.com/droppable/')

w1 = driver.current_window_handle
w2 = driver.find_element(By.XPATH, '//iframe[@class="demo-frame"]')
driver.switch_to.frame(frame_reference=w2)

t1 = WebDriverWait(
    driver=driver, 
    timeout=15, 
    poll_frequency=2.0
).until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@id="draggable"]')
    )
)

t2 = driver.find_element(By.XPATH, '//div[@id="droppable"]')

try:
    actionChains = ActionChains(driver=driver)
    actionChains.drag_and_drop(source=t1, target=t2).perform()
    time.sleep(3)
    driver.switch_to.window(window_name=w1)
except Exception as e:
    print("The Exception Is: ", e.__str__())
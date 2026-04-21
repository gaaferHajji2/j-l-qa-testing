from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.letskodeit.com/practice")
element = WebDriverWait(driver=driver, timeout=15).until(
    EC.presence_of_element_located((By.XPATH, '//select[@id="carselect"]'))
)
print("Select Element Of Car List Is: ", element)
time.sleep(2)

select_element = Select(element)
select_element.select_by_value('honda')
print("Select By Value: honda")
time.sleep(1)

# The Index Start From Zero.
# The Index Start From Zero And Index Can Be String.
select_element.select_by_index(1)
time.sleep(1)

select_element.select_by_visible_text('BMW')
print("Select By Visible Text: BMW")
time.sleep(1)
driver.quit()
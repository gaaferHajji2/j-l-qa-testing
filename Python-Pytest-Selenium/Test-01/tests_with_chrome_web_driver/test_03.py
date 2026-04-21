from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.letskodeit.com/practice")
print("The Title Of Page is: ", driver.title)
print("The Current URL Of Page Is: ", driver.current_url)

driver.get("https://www.letskodeit.com/")
print("The Current URL Of Page Is: ", driver.current_url)
driver.back()
print("The Current URL Of Page Is: ", driver.current_url)
driver.forward()
print("The Current URL Of Page Is: ", driver.current_url)
print("The Page Source Length Is: ", len(driver.page_source))
driver.quit()

# time.sleep(10)
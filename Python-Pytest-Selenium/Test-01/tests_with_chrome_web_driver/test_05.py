from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
# from selenium.webdriver import Keys;
import time;

service = Service(executable_path="chromedriver.exe");
driver = webdriver.Chrome(service=service);
driver.maximize_window();
driver.get("https://google.com/");
search_element = driver.find_element(By.XPATH, "//textarea[@id='APjFqb']");
search_element.send_keys("Testing Using Selenium And BS4");
img_element = driver.find_element(By.XPATH, "//img[@class='lnXdpd']");
img_element.click();
# img_element.is_displayed();
# img_element.is_enabled();
# img_element.is_selected();
search_btn = WebDriverWait(driver=driver, timeout=15).until(
    EC.presence_of_elements_located((By.XPATH, "//input[@name='btnK']"))
)
# driver.find_elements(By.XPATH, "//input[@name='btnK']");
# driver.implicitly_wait(5);
search_btn[1].click();
time.sleep(3);
print("The Current Page URL Is: ", driver.current_url);
driver.quit();
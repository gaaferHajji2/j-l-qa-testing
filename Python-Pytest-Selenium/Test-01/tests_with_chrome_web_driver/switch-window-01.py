from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
import time;

service = Service(executable_path='chromedriver.exe');
driver = webdriver.Chrome(service=service);
driver.maximize_window();
driver.get("https://www.letskodeit.com/practice");
w1 = driver.current_window_handle;
t1 = driver.find_element(By.ID, 'openwindow');
t1.click();

w2 = driver.window_handles;
for w in w2:
    if w not in w1:
        driver.switch_to.window(w);
        break;

t2 = WebDriverWait(driver=driver, timeout=25, poll_frequency=1).until(
    EC.presence_of_element_located((By.XPATH, '//input[@id="search"]'))
)
t2.send_keys("Python");
time.sleep(3);
driver.switch_to.window(w1);
driver.quit();
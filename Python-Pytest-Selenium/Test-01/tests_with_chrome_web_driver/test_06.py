from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
# from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;
import time;

service = Service(executable_path="chromedriver.exe");
driver = webdriver.Chrome(service=service);
driver.maximize_window();
driver.get("https://www.letskodeit.com/practice");
btn1 = driver.find_element(By.XPATH, "//input[@id='bmwradio']");
btn1.click();
btn2 = driver.find_element(By.XPATH, "//input[@id='bmwcheck']");
btn2.click();
btn3 = driver.find_element(By.XPATH, "//input[@id='hondacheck']");
btn3.click();

print("The State Of BTN 1 Is: ", btn1.is_selected());
print("The State Of BTN 2 Is: ", btn2.is_selected());
print("The State Of BTN 3 Is: ", btn3.is_selected());

time.sleep(3);
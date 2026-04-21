from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from selenium.webdriver.common.by import By;


service = Service(executable_path='chromedriver.exe');
driver = webdriver.Chrome(service=service);
driver.maximize_window();
driver.get("https://www.letskodeit.com/practice");
text_element = WebDriverWait(driver=driver, timeout=15).until(
    EC.presence_of_element_located((By.ID, 'displayed-text'))
);
print("Text Element Is: ", text_element);

hide_element = driver.find_element(By.XPATH, '//input[@id="hide-textbox"]');
show_element = driver.find_element(By.XPATH, '//input[@id="show-textbox"]');
print("Hide Element Is: ", hide_element);
print("Show Element Is: ", show_element);
print("The State Of Text Element Is: ", text_element.is_displayed());

hide_element.click();
print("The State Of Text Element Is: ", text_element.is_displayed());
show_element.click();
print("The State Of Text Element Is: ", text_element.is_displayed());
driver.quit();
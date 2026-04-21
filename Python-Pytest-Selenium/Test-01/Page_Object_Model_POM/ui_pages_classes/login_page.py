from selenium.webdriver.common.by import By
from ui_pages_classes.base_class import BasePageClass

class LoginPage(BasePageClass):

    LOGIN_LINK = (By.XPATH, "//a[text()='Sign In']")
    EMAIL_ADDRESS = (By.XPATH, "//input[@placeholder='Email Address']")
    PASSWORD = (By.XPATH, "//input[@id='login-password']")
    LOGIN_BTN = (By.XPATH, "//button[@id='login']")

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def click_login_link(self):
        self.click(self.LOGIN_LINK)
    
    def enter_email_addr(self, email: str = ""):
        self.send_keys(locator=self.EMAIL_ADDRESS, text=email)
    
    def enter_password(self, password: str = ""):
        self.send_keys(locator=self.PASSWORD, text=password)
    
    def click_login_btn(self):
        self.click(self.LOGIN_BTN)
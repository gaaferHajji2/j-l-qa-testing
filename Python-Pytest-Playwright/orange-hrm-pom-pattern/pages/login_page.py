from playwright.async_api import expect
from pages.base_page import BasePage
from utils.logger import logger

class LoginPage(BasePage):
    LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    DASHBOARD_URL = "**/dashboard/index"
    USERNAME_PALCEHOLDER = "Username"
    PASSWORD_PALCEHOLDER = "Password"
    SUBMIT_BUTTON_LOCATOR = "button[type='submit']"
    ERROR_TEXT = "Invalid credentials"

    async def navigate_to_login(self):
        await self.navigate_to(self.LOGIN_URL)

    async def login(self, username: str, password: str):
        logger.info(f"Step 1: Entering username '{username}'")
        await self.page.get_by_placeholder(self.USERNAME_PALCEHOLDER).fill(username)

        logger.info("Step 2: Entering password")
        await self.page.get_by_placeholder(self.PASSWORD_PALCEHOLDER).fill(password)

        logger.info("Step 3: Clicking Login button")
        await self.page.locator(self.SUBMIT_BUTTON_LOCATOR).click()

        # Wait for navigation
        await self.page.wait_for_url(self.DASHBOARD_URL, timeout=10000)
        logger.info("✅ Login successful - redirected to Dashboard")

    async def get_error_message(self):
        error = self.page.get_by_text(self.ERROR_TEXT)
        await expect(error).to_be_visible(timeout=5000) # need refactor
        text = await error.inner_text()
        logger.info(f"Error message displayed: {text}")
        return text

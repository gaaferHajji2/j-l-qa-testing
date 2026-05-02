from playwright.async_api import expect
from pages.base_page import BasePage
from utils.logger import logger

class DashboardPage(BasePage):
    async def verify_dashboard_loaded(self):
        logger.info("Step: Verifying Dashboard page")
        header = self.page.get_by_role("heading", name="Dashboard")
        await expect(header).to_be_visible(timeout=10000)
        await self.take_screenshot("dashboard_loaded")  # Required screenshot
        logger.info("✅ Dashboard loaded successfully")

    async def navigate_to_admin(self):
        logger.info("Step: Clicking Admin menu")
        await self.page.locator("//span[normalize-space()='Admin']").click()
        await self.page.wait_for_url("**/admin/viewSystemUsers", timeout=10000)
        await expect(self.page.get_by_role("heading", name="Admin")).to_be_visible()
        await self.take_screenshot("admin_page")
        logger.info("✅ Navigated to Admin module")

    async def navigate_to_pim(self):
        logger.info("Step: Clicking PIM menu")
        await self.page.locator("//span[normalize-space()='PIM']").click()
        await self.page.wait_for_url("**/pim/viewEmployeeList", timeout=10000)
        await expect(self.page.get_by_role("heading", name="Employee Information")).to_be_visible()
        await self.take_screenshot("pim_page")
        logger.info("✅ Navigated to PIM (Employee List)")

    async def logout(self):
        logger.info("Step: Opening user dropdown")
        await self.page.locator(".oxd-userdropdown-name").click()
        logger.info("Step: Clicking Logout")
        await self.page.get_by_text("Logout").click()
        await self.page.wait_for_url("**/auth/login", timeout=10000)
        logger.info("✅ Logout successful")

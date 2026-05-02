from abc import ABC
from datetime import datetime
from playwright.async_api import Page
from utils.logger import logger

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page

    async def navigate_to(self, url: str):
        await self.page.goto(url, wait_until="networkidle")
        logger.info(f"Navigated to: {url}")

    async def take_screenshot(self, name: str):
        """Manual screenshot for key verification steps"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/{name}_{timestamp}.png"
        await self.page.screenshot(path=path)
        logger.info(f"Screenshot captured: {path}")
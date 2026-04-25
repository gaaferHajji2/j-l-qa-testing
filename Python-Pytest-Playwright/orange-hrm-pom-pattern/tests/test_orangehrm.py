import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger

@pytest.mark.asyncio
async def test_successful_login_and_verify_dashboard(page):
    """Test 1: Valid login + Dashboard verification"""
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    await login_page.navigate_to_login()
    await login_page.login("Admin", "Admin123")
    await dashboard_page.verify_dashboard_loaded()
    logger.info("✅ Test 1 PASSED")

@pytest.mark.asyncio
async def test_invalid_login_shows_error(page):
    """Test 2: Invalid credentials error"""
    login_page = LoginPage(page)
    await login_page.navigate_to_login()
    await login_page.login("Admin", "WrongPass123")
    error = await login_page.get_error_message()
    assert "Invalid credentials" in error
    await login_page.take_screenshot("invalid_login_error")  # Required screenshot
    logger.info("✅ Test 2 PASSED")

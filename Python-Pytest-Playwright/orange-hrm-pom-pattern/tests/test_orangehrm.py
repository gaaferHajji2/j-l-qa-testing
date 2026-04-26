import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import logger

@pytest.mark.asyncio
async def test_successful_login_and_verify_dashboard(page):
    """Test 1: Valid login + Dashboard verification"""
    login_page = LoginPage(page)
    logger.info("1 ==> successful login ==> Creating Login Page")
    dashboard_page = DashboardPage(page)
    logger.info("2 ==> successful login ==> Creating Dashboard Page")

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

@pytest.mark.asyncio
async def test_navigate_to_admin_module(logged_in_page):
    """Test 3: Navigate to Admin module (uses logged-in fixture)"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.navigate_to_admin()
    logger.info("✅ Test 3 PASSED")

@pytest.mark.asyncio
async def test_navigate_to_pim_module(logged_in_page):
    """Test 4: Navigate to PIM (Employee List)"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.navigate_to_pim()
    logger.info("✅ Test 4 PASSED")

@pytest.mark.asyncio
async def test_logout_functionality(logged_in_page):
    """Test 5: Full logout flow"""
    dashboard_page = DashboardPage(logged_in_page)
    await dashboard_page.logout()
    # Verify back on login page
    await logged_in_page.check_username_element()
    await dashboard_page.take_screenshot("after_logout")
    logger.info("✅ Test 5 PASSED")

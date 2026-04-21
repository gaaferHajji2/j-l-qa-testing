from playwright.sync_api import sync_playwright
import time
import re

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://bootswatch.com/default/")

    btn = page.get_by_role('button', name='Default button')
    btn.scroll_into_view_if_needed()
    print("The Button Is: ", btn)

    heading = page.get_by_role('heading', name='Heading 2')
    heading.scroll_into_view_if_needed()
    print("The Heading Is: ", heading)

    radio_btn = page.get_by_role('radio', name=re.compile("^(Option One)", re.IGNORECASE))
    radio_btn.scroll_into_view_if_needed()
    print("The Radio BTN Is: ", radio_btn)
    print("The Radio BTN is_visible Is: ", radio_btn.is_visible())

    checkbox = page.get_by_role('checkbox', name=re.compile("Default Checkbox", re.IGNORECASE))
    checkbox.scroll_into_view_if_needed()
    # checkbox has method name: check()-method that check/uncheck the status of checkbox
    print("The Checkbox Is: ", checkbox)
    print("The Checkbox is_visible Is: ", checkbox.is_visible())

    # This Will Throw An Exception If Multiple Elements
    # Are Selected By The Role
    # email_input = page.get_by_label("Email address")
    # email_input.scroll_into_view_if_needed()
    # email_input.highlight()

    password_input = page.locator("#floatingPassword")
    password_input.scroll_into_view_if_needed()
    password_input.highlight()

    email_input_by_placeholder = page.get_by_placeholder("name@example.com")
    email_input_by_placeholder.scroll_into_view_if_needed()
    email_input_by_placeholder.highlight()

    text_element = page.get_by_text("with faded secondary text")
    text_element.scroll_into_view_if_needed()
    text_element.highlight()

    middle_element = page.get_by_text("Middle")
    middle_element.scroll_into_view_if_needed()
    middle_element.highlight()

    text_element = page.get_by_text("attr", exact=True)
    print("The element with exact is, display: ", text_element.is_visible())
    text_element.scroll_into_view_if_needed()
    text_element.highlight()

    # password_input_by_placeholder = page.get_by_placeholder("Password")

    # password_input_by_placeholder.highlight()

    time.sleep(1)

    page.close()
    browser.close()
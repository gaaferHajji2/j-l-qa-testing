from playwright.sync_api import Page, expect

def test_search_element(page: Page):
    page.goto("https://playwright.dev/python/")

    input = page.get_by_placeholder("Search docs")
    expect(input).to_be_hidden()

    search_btn = page.get_by_role('button', name="Search")
    search_btn.press('Control+KeyK')

    expect(input).to_be_editable()
    expect(input).to_be_empty()

    query = "Async API"
    input.fill(query)

    expect(input).to_have_value(query)
from playwright.sync_api import Page, expect

def test_multi_select_list(page: Page):
    page.goto("https://bootswatch.com/default/")

    multi_select_list = page.get_by_label("Example multiple select")
    multi_select_list.scroll_into_view_if_needed()
    multi_select_list.select_option(["1", "2", "3"])
    expect(multi_select_list).to_have_values(["1", "2", "3"])
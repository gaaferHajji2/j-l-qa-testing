from time import perf_counter
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright1:
    browser = playwright1.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    
    print("Page Loading...")
    start = perf_counter()
    page.goto("https://bootswatch.com/", wait_until='load')
    print(f"Total Time For Load Event Is: {round(perf_counter() - start, 2)}")

with sync_playwright() as playwright2:
    browser = playwright2.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    
    print("Page Loading...")
    start = perf_counter()
    page.goto("https://bootswatch.com/", wait_until='commit')
    print(f"Total Time For commit Event Is: {round(perf_counter() - start, 2)}")

with sync_playwright() as playwright3:
    browser = playwright3.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    
    print("Page Loading...")
    start = perf_counter()
    page.goto("https://bootswatch.com/", wait_until='networkidle')
    print(f"Total Time For NetworkIdle Event Is: {round(perf_counter() - start, 2)}")

with sync_playwright() as playwright4:
    browser = playwright4.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    
    print("Page Loading...")
    start = perf_counter()
    page.goto("https://bootswatch.com/", wait_until='domcontentloaded')
    print(f"Total Time For DOM Content Loaded Event Is: {round(perf_counter() - start, 2)}")
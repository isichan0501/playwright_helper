from playwright.sync_api import sync_playwright

def run(playwright):
    iphone_13 = playwright.devices['iPhone 13']
    import pdb;pdb.set_trace()
    browser = playwright.webkit.launch(headless=False)
    context = browser.new_context(
        **iphone_13,
    )

with sync_playwright() as playwright:
    run(playwright)
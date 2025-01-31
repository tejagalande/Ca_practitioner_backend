from playwright.sync_api import sync_playwright

def run(playwright):
    # Set up the proxy with authentication
    proxy = {
        "server": "http://in-pr.oxylabs.io:30001",
        "username": "customer-tejas_Icon22",
        "password": "Overview=RP250"
    }

    try:
        # Launch the browser with the proxy settings
        browser = playwright.chromium.launch(headless=False, proxy=proxy)
        context = browser.new_context()

        # Open a new page
        page  = context.new_page()

        # Navigate to a test URL (you can replace this with your target URL)
        page.goto("https://services.gst.gov.in/services/login")
        page.wait_for_timeout(timeout=2000)
        print("Proxy setup seems correct. Page loaded successfully.")
    except Exception as e:
        print('Error - ',e)
    finally:

        # Close the browser
        browser.close()

# Running the function with Playwright
with sync_playwright() as playwright:
    run(playwright)

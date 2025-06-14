from playwright.sync_api import sync_playwright

def execute_actions(url, actions):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        for step in actions:
            action = step.get("action")
            selector_id = step.get("selector_id")
            value = step.get("value", "")

            selector = f"[data-label-id='{selector_id}']"
            try:
                if action == "fill":
                    page.fill(selector, value)
                    print(f"Filled selector {selector} with value: {value}")
                elif action == "click":
                    page.click(selector)
                    print(f"Clicked selector {selector}")
            except Exception as e:
                print(f"[!] Failed on action {step}: {e}")

        page.wait_for_timeout(5000)
        browser.close()

from playwright.sync_api import sync_playwright
import uuid

def get_dom_elements_with_boxes(url):
    elements_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        elements = page.query_selector_all("input, textarea, select, button")

        for idx, el in enumerate(elements):
            try:
                box = el.bounding_box()
                el.set_attribute("data-label-id", str(idx))
                el.evaluate(
                    '''(el, idx) => {
                        el.style.border = "2px solid red";
                        let label = document.createElement("div");
                        label.innerText = idx;
                        label.style.position = "absolute";
                        label.style.background = "yellow";
                        label.style.left = (el.offsetLeft) + "px";
                        label.style.top = (el.offsetTop - 20) + "px";
                        label.style.zIndex = "9999";
                        label.style.fontSize = "12px";
                        document.body.appendChild(label);
                    }''', idx
                )

                tag = el.evaluate("e => e.tagName.toLowerCase()")
                typ = el.get_attribute("type") or ""
                name = el.get_attribute("name") or ""
                placeholder = el.get_attribute("placeholder") or ""

                elements_data.append({
                    "selector_id": str(idx),
                    "tag": tag,
                    "type": typ,
                    "name": name,
                    "placeholder": placeholder,
                })

            except Exception as e:
                print(f"[!] Failed to process element {idx}: {e}")
        
        page.screenshot(path=f"screenshot_{uuid.uuid4().hex}.png", full_page=True)
        browser.close()

    return elements_data

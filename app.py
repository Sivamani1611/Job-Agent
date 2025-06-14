import json
from browser.executor import execute_actions
from llm.openrouter_llm import query_openrouter
from resume_parser.parser import extract_resume_data
from browser.playwright_driver import get_dom_elements_with_boxes

def main():
    resume_path = "resume.pdf"
    urls_path = "urls.txt"
    resume_data = extract_resume_data(resume_path)

    with open(urls_path, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    for url in urls:
        print(f"\n--- Processing: {url} ---")
        dom = get_dom_elements_with_boxes(url)
        prompt = build_prompt(resume_data, dom, url)
        response = query_openrouter(prompt)

        try:
            actions = json.loads(response)
            print("Executing actions:", actions)
            execute_actions(url, actions)
        except json.JSONDecodeError:
            print("[!] LLM did not return valid JSON. Skipping this URL.")
            print("LLM Response:", response)

def build_prompt(resume_data, dom_elements, url):
    return f"""
You are an automation agent tasked with applying for a job using the following resume data:

Name: {resume_data["name"]}
Email: {resume_data["email"]}
Phone: {resume_data["phone"]}
Skills: {resume_data["skills"]}

The job application form is on this page: {url}
Below is a JSON list of interactive DOM elements on the page:

{json.dumps(dom_elements, indent=2)}

Determine:
1. Which elements match the resume fields
2. What data to insert into each
3. The order of actions

Reply ONLY with a JSON array like:
[
  {{ "action": "fill", "selector_id": "3", "value": "John Doe" }},
  {{ "action": "click", "selector_id": "5" }}
]
"""

if __name__ == "__main__":
    main()

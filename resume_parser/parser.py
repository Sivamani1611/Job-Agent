# Extracts data from resume PDF
import fitz  # PyMuPDF
import re

def extract_resume_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    name = re.findall(r"(?:Name|Full Name)[:\\s]*([A-Z][a-z]+(?: [A-Z][a-z]+)+)", text)
    email = re.findall(r"[\\w.-]+@[\\w.-]+\\.\\w+", text)
    phone = re.findall(r"\\+?\\d[\\d\\s-]{8,}\\d", text)
    skills = re.findall(r"(Skills|Technical Skills)[:\\s]*(.*)", text, re.IGNORECASE)

    return {
        "name": name[0] if name else "",
        "email": email[0] if email else "",
        "phone": phone[0] if phone else "",
        "skills": skills[0][1] if skills else ""
    }

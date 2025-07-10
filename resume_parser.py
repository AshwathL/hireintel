import fitz  # PyMuPDF
import re
from dotenv import load_dotenv
import os
import spacy

load_dotenv()

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'(\+91[-\s]?)?[0]?[6789]\d{9}', text)
    return match.group() if match else None

def extract_name(text):
    lines = text.strip().split("\n")
    email = extract_email(text)
    phone = extract_phone(text)

    # Step 1: Find line that contains email or phone
    name_line = None
    for i, line in enumerate(lines):
        if email and email in line or phone and phone in line:
            # Check 2 lines above this block for likely name
            for j in range(i-6, i+1):
                if 0 <= j < len(lines):
                    candidate = lines[j].strip()
                    # Valid if not too long, no numbers or links
                    if candidate and len(candidate.split()) <= 4 and not re.search(r'\d|@|http', candidate, re.I):
                        name_line = candidate
                        break
            break

    if name_line:
        return name_line.strip().title()

    # Fallback 1: Look at filename
    return "Unknown"




def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "raw_text": text
    }

if __name__ == "__main__":
    resume_path = r"D:\Hireintel\resumes\Haripriya_resume_proj.pdf"
    data = parse_resume(resume_path)
    print(data)

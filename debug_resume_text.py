import fitz  # PyMuPDF
import sys

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    resume_path = "resumes/Haripriya_resume_proj.pdf"  # replace with any problematic file
    full_text = extract_text_from_pdf(resume_path)

    print("\n========== FULL RAW TEXT ==========\n")
    print(full_text)

    # Optional: print first 15 lines with line numbers
    print("\n========== FIRST 15 LINES ==========\n")
    lines = full_text.strip().split("\n")
    for i, line in enumerate(lines[:15]):
        print(f"{i+1:>2}: {line.strip()}")

import sys
import os
import requests
import json
from dotenv import load_dotenv
import re

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def extract_json(raw_text):
    match = re.search(r"\{[\s\S]*?\}", raw_text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("⚠️ LLM returned invalid JSON block.")
            return {}
    return {}

def match_resume_to_jd(jd_data, resume_data, model="deepseek/deepseek-chat-v3-0324:free"):
    # Parse jd_data if it's a JSON string
    if isinstance(jd_data, str):
        print(f"Debug: jd_data type: {type(jd_data)}")
        print(f"Debug: jd_data content: {repr(jd_data)}")
        if jd_data.strip():  # Check if string is not empty
            # Handle markdown-wrapped JSON
            if jd_data.strip().startswith('```json'):
                # Extract JSON from markdown code blocks
                json_content = jd_data.strip()
                json_content = json_content.replace('```json', '').replace('```', '').strip()
                jd_data = json_content
            
            try:
                jd_data = json.loads(jd_data)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Raw content: {jd_data}")
                raise Exception(f"Invalid JSON returned from analyze_job_description: {jd_data}")
        else:
            raise Exception("Empty response from analyze_job_description")
    
    prompt = f"""
You are an expert AI recruiter.

Compare the following **resume** with the **job description info**.

=== JOB DESCRIPTION ===
Job Title: {jd_data['job_title']}
Required Skills: {', '.join(jd_data['required_skills'])}
Preferred Skills: {', '.join(jd_data['preferred_skills'])}
Years of Experience: {jd_data['years_of_experience']}
Keywords: {', '.join(jd_data['industry_keywords'])}

=== CANDIDATE RESUME ===
Name: {resume_data['name']}
Email: {resume_data['email']}
Phone: {resume_data['phone']}

Resume Content:
{resume_data['raw_text']}

Return a JSON with:
- match_score (0–100)
- matched_skills
- missing_skills
- strengths
- red_flags
- summary_verdict
- an overall score out of 100
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a smart AI recruiter who evaluates candidates."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        result = response.json()
        raw_content = result['choices'][0]['message']['content']
        parsed_json = extract_json(raw_content)

        if not parsed_json:
            print("⚠️ No valid JSON found in LLM response:")
            print(raw_content)

        return parsed_json  # ✅ return dict, not string
    else:
        raise Exception(f"OpenRouter Error: {response.status_code} — {response.text}")

if __name__ == "__main__":
    from resume_parser import parse_resume
    from jd_analyser import analyze_job_description

    resume_path = r"D:\Hireintel\Ashwath_L_Resume_ML.pdf"
    jd_text = """
We are hiring a Data Scientist to join our analytics team. Candidates should have experience in Python, SQL, machine learning, and data visualization. Preferred: knowledge of cloud platforms like AWS or GCP. Minimum 2 years of experience required.
"""

    resume = parse_resume(resume_path)
    jd_data = analyze_job_description(jd_text)

    result = match_resume_to_jd(jd_data, resume)
    print(result)

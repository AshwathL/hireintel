import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_interview_questions(jd_data, resume_data, model="deepseek/deepseek-chat-v3-0324:free"):
    prompt = f"""
You are an AI recruiter assistant.

Based on the following **Job Description** and **Candidate Resume**, generate:
- 5 technical interview questions
- 3 behavioral interview questions
- 2 bonus/domain-specific questions

Use the job requirements and candidate profile to tailor the questions.

=== JOB DESCRIPTION ===
Job Title: {jd_data['job_title']}
Required Skills: {', '.join(jd_data['required_skills'])}
Preferred Skills: {', '.join(jd_data['preferred_skills'])}
Years of Experience: {jd_data['years_of_experience']}
Industry Keywords: {', '.join(jd_data['industry_keywords'])}

=== CANDIDATE RESUME ===
Name: {resume_data['name']}
Email: {resume_data['email']}

Resume Content:
{resume_data['raw_text']}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a smart AI recruiter generating interview questions."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
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

    print(f"Debug: jd_data content: {repr(jd_data)}")

    if isinstance(jd_data, str):
        jd_data = jd_data.strip()
        if jd_data.startswith('```json'):
            jd_data = jd_data.replace('```json', '').replace('```', '').strip()
        if jd_data:
            jd_data = json.loads(jd_data)
        else:
            raise Exception("Empty response from analyze_job_description")

    questions = generate_interview_questions(jd_data, resume)
    print("\n📋 INTERVIEW QUESTIONS:")
    print(questions)

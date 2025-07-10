import os
import requests
from dotenv import load_dotenv
import re
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def extract_json(raw_text):
    # Find the first JSON-looking block
    match = re.search(r"\{[\s\S]*\}", raw_text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {}
    return {}

def analyze_job_description(jd_text, model="deepseek/deepseek-chat-v3-0324:free"):
    prompt = f"""
You are an AI HR assistant. Extract structured information from this job description:

Job Description:
\"\"\"
{jd_text}
\"\"\"

Return output in JSON with these fields:
- job_title
- required_skills (list)
- preferred_skills (list)
- years_of_experience
- industry_keywords (list)
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for hiring."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        result = response.json()
        raw_output = result['choices'][0]['message']['content']
        return extract_json(raw_output)  # ✅ parsed JSON dict
    else:
        raise Exception(f"OpenRouter Error: {response.status_code} — {response.text}")

if __name__ == "__main__":
    jd_text = """
We are hiring a Data Scientist to join our analytics team. Candidates should have experience in Python, SQL, machine learning, and data visualization. Preferred: knowledge of cloud platforms like AWS or GCP. Minimum 2 years of experience required.
"""
    result = analyze_job_description(jd_text)
    print(result)

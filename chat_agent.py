import json
import os
from glob import glob
from dotenv import load_dotenv
import requests
from resume_parser import parse_resume
from jd_analyser import analyze_job_description

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_agent(user_query, jd_data, resume_list, model="deepseek/deepseek-chat-v3-0324:free"):
    prompt = f"""
You are a smart AI recruiter assistant. You are analyzing the following job description and {len(resume_list)} candidate resumes.

JOB DESCRIPTION:
{json.dumps(jd_data, indent=2)}

CANDIDATE RESUMES:
{json.dumps(resume_list, indent=2)}

Answer the user's question below as accurately and clearly as possible.

USER QUESTION:
{user_query}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an intelligent hiring assistant for a recruiter."},
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
    # Load JD
    with open("jd.txt", "r", encoding="utf-8") as f:
        jd_text = f.read()
    jd_json = analyze_job_description(jd_text)

    if isinstance(jd_json, str):
        jd_json = jd_json.strip()
        if jd_json.startswith("```json"):
            jd_json = jd_json.replace("```json", "").replace("```", "").strip()
        jd_data = json.loads(jd_json)
    else:
        jd_data = jd_json

    # Load resumes
    resume_files = glob("resumes/*.pdf")
    resumes = []
    for r in resume_files:
        parsed = parse_resume(r)
        resumes.append(parsed)

    # Chat loop
    print("🤖 HireIntel Chat Agent Ready. Type your question or 'exit' to quit.")
    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting. Bye!")
            break
        try:
            answer = ask_agent(user_input, jd_data, resumes)
            print(f"\n🤖 Agent:\n{answer}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

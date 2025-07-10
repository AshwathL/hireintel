import json, os, requests, pandas as pd
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"

def rank_resumes(match_results, model="deepseek/deepseek-chat-v3-0324:free"):
    """
    match_results → list[dict] each produced by matcher_agent
      expected keys: name, email, match_score, strengths, red_flags, summary_verdict
    returns ordered list plus LLM summary of why the order makes sense
    """

    # 1️⃣ rank locally with pandas (no LLM tokens)
    df = pd.DataFrame(match_results)
    df_sorted = df.sort_values("match_score", ascending=False).reset_index(drop=True)

    # 2️⃣ create a tiny prompt ONLY with aggregated rows → minimal tokens
    table_for_llm = df_sorted[["name", "match_score", "strengths", "red_flags"]].to_json(orient="records")

    prompt = f"""
You are an AI hiring assistant. Here is a JSON list of candidates already scored:

{table_for_llm}

Write:
1. A short ranked list (best → worst) with score in parentheses.
2. 1‑sentence reason each top‑3 are strong.
3. 1‑sentence reason the bottom candidate is not a fit.
Return plain markdown.
"""

    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}",
               "Content-Type": "application/json"}

    body = {"model": model,
            "messages":[
                {"role":"system","content":"You are a concise HR analyst."},
                {"role":"user","content":prompt}
            ]}

    resp = requests.post(URL, headers=headers, json=body)
    resp.raise_for_status()
    narrative = resp.json()["choices"][0]["message"]["content"]

    return df_sorted, narrative

# quick CLI test
if __name__ == "__main__":
    # pretend we already ran matcher_agent on two résumés
    fake = [
        {"name":"Aarav","email":"aarav@x.com","match_score":82,
         "strengths":"Python + SQL","red_flags":"no cloud exp","summary_verdict":"solid"},
        {"name":"Sneha","email":"sneh@y.com","match_score":67,
         "strengths":"viz whiz","red_flags":"little ML","summary_verdict":"needs training"}
    ]
    table, note = rank_resumes(fake)
    print(table[["name","match_score"]])
    print("\n---\n", note)

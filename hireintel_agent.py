import json
import os
from glob import glob
from resume_parser import parse_resume
from jd_analyser import analyze_job_description
from matcher_agent import match_resume_to_jd
from ranker_agent import rank_resumes
from interview_q_agent import generate_interview_questions

# Step 1: Load JD and analyze
with open("jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

print("🔍 Analyzing Job Description...\n")
jd_struct = analyze_job_description(jd_text)  

# Step 2: Load and parse resumes
resume_files = glob("resumes/*.pdf")
results = []

for resume_path in resume_files:
    print(f"📄 Parsing: {os.path.basename(resume_path)}")
    parsed_resume = parse_resume(resume_path)

    print("🤖 Matching resume to JD...")
    match_data = match_resume_to_jd(jd_struct, parsed_resume, model="deepseek/deepseek-chat-v3-0324:free")
    
    match_data["name"] = parsed_resume.get("name", "Unknown")
    match_data["email"] = parsed_resume.get("email", "N/A")
    match_data["raw_text"] = parsed_resume["raw_text"]

    results.append(match_data)

# Step 3: Rank candidates
print("\n📊 Ranking candidates based on fit...")
table, summary = rank_resumes(results, model="deepseek/deepseek-chat-v3-0324:free")

# Step 4: Output results
print("\n🏆 Top Candidates:")
print(table[["name", "match_score"]])
print("\n📝 Ranking Summary:\n")
print(summary)

# Step 5: Generate Interview Questions (optional)
print("\n🧠 Generating Interview Questions for Top Candidate...\n")
top_candidate = results[0]
questions = generate_interview_questions(jd_struct, top_candidate, model="deepseek/deepseek-chat-v3-0324:free")
print(questions)

# Optional Step: Save report
with open("results_summary.md", "w", encoding="utf-8") as f:
    f.write(f"# HireIntel Report\n\n")
    f.write(f"## Ranked Candidates\n\n")
    f.write(table[["name", "match_score"]].to_markdown(index=False))
    f.write(f"\n\n## Summary\n\n{summary}\n")
    f.write(f"\n\n## Interview Questions for {top_candidate['name']}\n\n{questions}")

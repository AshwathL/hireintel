import os
import json
from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
from resume_parser import parse_resume
from jd_analyser import analyze_job_description
from chat_agent import ask_agent
from glob import glob

app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'uploads'
RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
JD_FILE = os.path.join(UPLOAD_FOLDER, 'jd.txt')

os.makedirs(RESUME_FOLDER, exist_ok=True)

# Global variables to hold processed data
parsed_jd = None
parsed_resumes = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_data():
    global parsed_jd, parsed_resumes

    # Save JD
    jd_text = request.form.get("job_description")
    with open(JD_FILE, "w", encoding="utf-8") as f:
        f.write(jd_text)

    jd_json = analyze_job_description(jd_text)
    if isinstance(jd_json, str):
        jd_json = jd_json.strip()
        if jd_json.startswith("```json"):
            jd_json = jd_json.replace("```json", "").replace("```", "").strip()
        parsed_jd = json.loads(jd_json)
    else:
        parsed_jd = jd_json

    # Save resumes
    parsed_resumes = []
    resume_files = request.files.getlist("resumes")
    for file in resume_files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(RESUME_FOLDER, filename)
        file.save(filepath)
        parsed = parse_resume(filepath)
        parsed_resumes.append(parsed)

    return redirect("/chat")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/chat_api", methods=["POST"])
def chat_api():
    global parsed_jd, parsed_resumes

    user_input = request.json.get("message", "")
    try:
        answer = ask_agent(user_input, parsed_jd, parsed_resumes)
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

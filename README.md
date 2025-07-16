# 💼 HireIntel — Your Smart Hiring Agent

**HireIntel** is an AI-powered recruitment assistant that helps recruiters streamline the candidate selection process by intelligently analyzing job descriptions and resumes. It also allows recruiters to chat with a smart hiring agent to get insights, rankings, and answers to queries about the candidates.

---

## 🚀 Features

- ✅ Upload multiple resumes (PDF format)
- ✅ Input a job description manually
- ✅ Extract structured data using NLP
- ✅ Rank candidates based on job fit
- ✅ Chat with a smart hiring agent
- ✅ Clean UI with light/dark mode toggle

---

## 🖼 Demo Preview

> 📷 _You can add a hosted link or screenshot here once deployed on Render._

---

## 🛠 Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **AI Model**: OpenRouter LLMs (e.g., DeepSeek Chat)
- **NLP**: spaCy (`en_core_web_sm`)
- **Hosting**: Render

---

## 📂 Project Structure

HireIntel/
├── app.py
├── resume_parser.py
├── jd_analyser.py
├── hireintel_agent.py
├── requirements.txt
├── setup.sh
├── templates/
│ ├── index.html
│ ├── chat.html
│ ├── style.css
│ └── script.js
├── uploads/
│ └── (temporary resumes + JD)
└── .env (excluded from repo)

---

## 🧪 Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/AshwathL/hireintel.git
cd hireintel
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```
### 4. Add .env file
Create a .env file in root with:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
## 5. Run the App
```bash
python app.py
```

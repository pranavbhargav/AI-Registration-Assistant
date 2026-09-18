# Internship Task Submission Guide: AI Registration Assistant

**Task ID:** AI-SS-001  
**Student Code:** DAS010164  
**Project Name:** AI Registration Assistant  
**Platform:** Free Online AI & Data Science Internship  

---

## 📋 Submission Checklist Overview

| Item | Requirement | Status |
| :--- | :--- | :---: |
| **Complete Source Code** | Python 3.10+, NLP Preprocessing, ML Classifier, FSM Dialog | ✅ Complete |
| **GitHub Repository** | Public repo with detailed README and Task Link | ✅ Ready to Push |
| **Project Report** | 1–2 page technical report (`REPORT.md`) | ✅ Complete |
| **Screenshots** | 5+ screenshots demonstrating different features | 📸 Ready to capture |
| **YouTube Video Demo** | Walkthrough showing code and live chatbot conversation | 📹 Script provided below |
| **Blog Post Submission** | Published on `https://www.freeinternships.in/blog/` | 📝 Draft provided below |

---

## 📝 1. Ready-to-Copy Blog Post

Submit this on **[https://www.freeinternships.in/blog/](https://www.freeinternships.in/blog/)**:
- **Category:** `Task Submit`
- **Title:** `AI Registration Assistant - DAS010164`

### Blog Post Body (Copy & Paste):

```markdown
# Building an Intelligent AI Registration Assistant using NLP & Machine Learning

**Task ID:** AI-SS-001  
**Student Code:** DAS010164  
**Internship Program:** Free Online AI & Data Science Internship  
**GitHub Repository:** https://github.com/pranavbhargav/AI-Registration-Assistant  
**Video Demo:** [Insert your YouTube Video Link here]  

---

## Introduction
As part of the Free Online AI & Data Science Internship, I built the **AI Registration Assistant (Task AI-SS-001)** — an intelligent conversational chatbot engineered to automate and personalize the internship registration process. 

Traditional static web forms are impersonal and cannot answer candidate questions about certificates, duration, or prerequisites. The AI Registration Assistant bridges this gap by combining Natural Language Processing (NLP), Machine Learning intent classification, contextual entity extraction, and stateful dialog management.

---

## System Features & Capabilities

### 1. NLP Preprocessing & Machine Learning Intent Classifier
- **Tokenization, Lemmatization, and Stopword Filtering:** Uses NLTK's `WordNetLemmatizer` to reduce text to root vocabulary.
- **Scikit-Learn ML Model:** Trains a `TfidfVectorizer` paired with a `LogisticRegression` classifier over 12 distinct intents (Greetings, FAQs, Feedback, Registration).
- **Rule-based Heuristic Fallback:** Ensures sub-millisecond responses for primary commands.

### 2. Contextual Entity Extraction & Validation
- **Candidate Name Extraction:** Identifies full names using conversational patterns (e.g., "My name is...") and alphabetic constraints.
- **Email Validation:** Implements RFC 5322 regex validation to reject invalid or mistyped email addresses.
- **Field & Experience Normalization:** Categorizes applicants into standardized domains (AI/ML, Data Science, Computer Science) and experience tiers.

### 3. Stateful Dialog Management & Slot-Filling
- Maintains non-blocking Finite State Machine (FSM) conversation flows (`IDLE` ➔ `AWAITING_NAME` ➔ `AWAITING_EMAIL` ➔ `AWAITING_FIELD` ➔ `AWAITING_EXPERIENCE` ➔ `CONFIRMATION`).
- Supports **mid-conversation FAQ interruptions**: A student can ask about internship duration or stipend midway through their registration, and the assistant answers before smoothly resuming the application.

### 4. Web Interface & Admin Dashboard
- Built with **Flask**, featuring a modern responsive chat window with interactive quick-action chips.
- Includes an **Admin Dashboard (`/admin`)** displaying key applicant metrics, real-time search filtering, interaction logs, and CSV export functionality.

---

## Technical Stack
- **Programming Language:** Python 3.10+
- **NLP & Machine Learning:** NLTK, Scikit-Learn
- **Web Framework:** Flask
- **Data Persistence:** JSON (`registrations.json`, `chat_logs.json`)

---

## Project Screenshots
[Insert your 5 project screenshots here]
1. Terminal CLI Interface
2. Modern Web Chat Interface
3. Entity Extraction & Validation Flow
4. Confirmation & JSON Database Record
5. Admin Analytics Dashboard

---

## Conclusion & Learnings
Building this project provided in-depth practical knowledge of:
- End-to-end NLP pipelines and text normalization.
- Vectorization and multi-class classification using Scikit-Learn.
- Designing stateful conversational dialog managers.
- Building unified APIs and web portals for AI applications.

Special thanks to the Free Online AI & Data Science Internship team for this enriching hands-on challenge!
```

---

## 📹 2. YouTube Video Demo Script (3–5 Minutes)

Record your screen using OBS Studio, Loom, or Windows Game Bar (`Win + G`):

### Video Structure:
1. **Introduction (0:00 – 0:45)**
   - *"Hello everyone! My name is Pranav Bhargav (Student Code: DAS010164). Today I am demonstrating my submission for Task AI-SS-001: The AI Registration Assistant for the Free Online AI & Data Science Internship."*
   - Show the GitHub repository and project structure.

2. **Code Walkthrough (0:45 – 1:45)**
   - Open `app.py` in your code editor:
     - Show the NLP preprocessing (`WordNetLemmatizer`, tokenization).
     - Show the Scikit-Learn intent classification model (`TfidfVectorizer` + `LogisticRegression`).
     - Explain the entity extraction functions (`extract_name`, `extract_email`, validation rules).
     - Show the Finite State Machine in `process_message`.

3. **Terminal CLI Demonstration (1:45 – 2:45)**
   - Run `python test_assistant.py` to show all automated tests passing.
   - Run `python app.py`:
     - Greet the bot (`"Hello!"`).
     - Ask an FAQ (`"How long is the internship?"` and `"Will I get a certificate?"`).
     - Start registration (`"I want to register"`).
     - Test invalid email handling (type `"wrong-email"`) ➔ Show bot prompting for valid email.
     - Provide valid email, field, and experience level.
     - Show registration confirmation.

4. **Web Interface & Admin Dashboard (2:45 – 4:00)**
   - Run `python web_app.py` and open `http://127.0.0.1:5000`:
     - Show the responsive dark UI and quick suggestion chips.
     - Send a query and demonstrate real-time response with confidence/sentiment tags.
     - Navigate to `http://127.0.0.1:5000/admin` (Admin Dashboard):
       - Highlight the total registrations counter, dialog turns, and sentiment distribution.
       - Demonstrate the real-time applicant search filter.
       - Click **"Export CSV"** to demonstrate downloadable records.

5. **Conclusion (4:00 – 4:30)**
   - *"All core and bonus features have been successfully tested and deployed. Thank you for watching!"*

---

## 📸 3. Screenshots Capture Guide (5+ Views)

Take 5 high-quality screenshots and save them into an `assets/` or `screenshots/` folder:

1. **Screenshot 1 - Terminal CLI Conversation:**
   - Run `python app.py` and capture greeting, registration, and confirmation in terminal.
2. **Screenshot 2 - Automated Tests Passing:**
   - Run `python test_assistant.py` showing `ALL TESTS PASSED WITH 100% SUCCESS!`.
3. **Screenshot 3 - Web Chat Interface:**
   - Open `http://127.0.0.1:5000` showing conversation bubbles and quick suggestion chips.
4. **Screenshot 4 - Admin Dashboard:**
   - Open `http://127.0.0.1:5000/admin` showing metric cards, applicant table, and chat logs.
5. **Screenshot 5 - Persistent Data in Editor:**
   - Open `registrations.json` and `chat_logs.json` side-by-side in VS Code showing structured records.

---

## 🐙 4. Git Push Instructions

Run these commands in PowerShell inside `AI-Registration-Assistant/` to push the completed project to your GitHub repository:

```powershell
git add .
git commit -m "Complete AI Registration Assistant: NLP, ML classifier, dialog FSM, Flask Web UI, Admin Dashboard, and documentation"
git push origin main
```

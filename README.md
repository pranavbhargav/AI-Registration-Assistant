# AI Registration Assistant 🤖

**Task ID:** AI-SS-001  
**Student Code:** DAS010164  
**Internship Program:** Free Online AI & Data Science Internship  
**Official Task Link:** [Free AI & Data Science Internship Registration Assistant (AI-SS-001)](https://www.freeinternships.in/ai-data-science-internship/free-ai-data-science-internship-registration-assistant-ai-ss-001.php)

---

## 📌 Project Overview
The **AI Registration Assistant** is an intelligent conversational AI chatbot designed to guide students and applicants through the virtual internship registration process. Utilizing Natural Language Processing (NLP) fundamentals and machine learning, the assistant classifies user intents, answers frequently asked questions (FAQs), extracts and validates candidate entities, and records registrations into persistent structured storage.

The project offers **both an interactive command-line interface (CLI)** and a **modern, responsive web interface (Flask)** with a built-in **Admin Dashboard** and analytics suite.

---

## ✨ Features Implemented

### 🧠 Core Features
- **NLP Preprocessing Pipeline:** Text lowercasing, word tokenization, alphanumeric filtration, stopword removal, and word lemmatization using NLTK's `WordNetLemmatizer`.
- **Hybrid Intent Classification:**
  - **Scikit-Learn ML Model:** Dynamic training of a TF-IDF Vectorizer (`ngram_range=(1, 2)`) paired with a `LogisticRegression` classifier over intent patterns.
  - **Fast Rule-Based Fallback:** Pattern matching for zero-latency detection of common keywords.
- **Contextual Entity Extraction:**
  - **Name Extraction:** Uses conversational context parsing (e.g., `My name is [Name]`, `I am [Name]`) and capitalized string heuristics.
  - **Email Extraction:** RFC 5322 regex extraction with format validation.
  - **Field of Study Mapping:** Automatic normalization to standard domains (AI/ML, Data Science, Computer Science, IT, Electronics).
  - **Experience Level Categorization:** Maps user experience into Beginner, Intermediate, or Advanced tiers.
- **Strict Validation Checks:** Ensures valid email syntax, non-empty realistic names, and proper field lengths before moving forward.
- **Stateful Dialog Management (Finite State Machine):**
  - Non-blocking conversation flow (`IDLE` ➔ `AWAITING_NAME` ➔ `AWAITING_EMAIL` ➔ `AWAITING_FIELD` ➔ `AWAITING_EXPERIENCE` ➔ `CONFIRMATION`).
  - **Mid-Conversation FAQ Interruptions:** The bot answers questions like duration or certificates mid-dialog, then gently resumes the registration flow.
  - **Slot-Filling:** Automatically captures name or email if provided in the initial query.
- **Persistent Data Storage:** Stores registered candidate records in `registrations.json`.

### ⭐ Bonus Features
- **🌐 Web Interface (Flask):** Modern responsive web chat interface with quick suggestion chips, typing indicator animations, and responsive layout.
- **📊 Admin Dashboard (`/admin`):** Real-time candidate evaluation hub featuring key performance metrics, candidate search filter, interaction logs, and CSV export.
- **❤️ Sentiment Analysis:** Lexicon-based polarity detection that tailors empathetic conversational responses to user tone.
- **❓ Interactive FAQ Engine:** Responds to inquiries regarding internship duration, eligibility, verified certificates, stipend/fees, and required skills.
- **🌍 Multi-language Greetings:** Recognizes greetings in English, Hindi (`namaste`), Spanish (`hola`), and French (`bonjour`).
- **📈 Analytics & Logging:** Session tracking and intent confidence logging saved to `chat_logs.json`.

---

## 🏛️ System Architecture

```text
                                  ┌────────────────────────┐
                                  │   User Message / Query │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                    ┌──────────────────────────────────────────────────┐
                    │               NLP Preprocessing Engine           │
                    │  • Lowercase   • Tokenize   • Lemmatize (WordNet)│
                    │  • Stopword Filtration                           │
                    └───────────┬──────────────────────────┬───────────┘
                                │                          │
                                ▼                          ▼
        ┌───────────────────────────────┐  ┌───────────────────────────────┐
        │  Hybrid Intent Classification │  │   Entity Extraction & Regex   │
        │  • Scikit-Learn TF-IDF + ML   │  │  • Name  • Email (RFC 5322)   │
        │  • Heuristic Fallback Match   │  │  • Field • Experience Level   │
        └───────────────┬───────────────┘  └───────────────┬───────────────┘
                        │                                  │
                        └─────────────────┬────────────────┘
                                          ▼
                    ┌──────────────────────────────────────────┐
                    │         Stateful Dialog Manager          │
                    │   Finite State Machine & Slot-Filling    │
                    │   (Supports Mid-Conversation FAQs)       │
                    └───────────┬──────────────────┬───────────┘
                                │                  │
                ┌───────────────▼────────┐ ┌───────▼────────────────┐
                │   registrations.json   │ │     chat_logs.json     │
                │  (Applicant Profiles)  │ │ (Interaction Analytics)│
                └────────────────────────┘ └────────────────────────┘
```

---

## 📂 Project Structure

```text
AI-Registration-Assistant/
│
├── app.py                  # Core Conversational AI engine, NLP pipeline & CLI runner
├── web_app.py              # Flask web server exposing Chat UI, API & Admin routes
├── test_assistant.py       # Automated unit & integration test suite
├── intents.json            # Knowledge base and training utterances for intent classifier
├── registrations.json      # Persistent storage for registered student candidates
├── chat_logs.json          # Conversation logs and analytics telemetry
├── requirements.txt        # Python package dependencies
├── REPORT.md               # 1-2 page comprehensive project report
├── SUBMISSION_GUIDE.md     # Blog post draft, YouTube script, and screenshot checklist
├── templates/
│   ├── index.html          # Web chat interface
│   └── admin.html          # Admin dashboard & analytics view
└── README.md               # Project documentation
```

---

## 🚀 Quickstart & Installation

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/pranavbhargav/AI-Registration-Assistant.git
cd AI-Registration-Assistant

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
Verify all NLP, ML classification, entity validation, and dialog transitions:
```bash
python test_assistant.py
```

### 4. Option A: Run Terminal Assistant (CLI)
Launch the interactive command-line chatbot:
```bash
python app.py
```

### 5. Option B: Run Web Interface & Admin Dashboard (Flask)
Launch the web server:
```bash
python web_app.py
```
- Open **Chat Interface:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- Open **Admin Dashboard:** [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

---

## 💬 Sample Interaction Transcript

```text
Bot: Hello! Welcome to the AI & Data Science Internship Registration Assistant. How can I help you today?

You: I want to register for the internship
Bot: Awesome! I'll guide you step-by-step through the internship registration. First, what is your full name?

You: Wait, how long is the internship duration?
Bot: The AI & Data Science Internship follows a flexible 1-week to 4-week self-paced milestone structure with hands-on tasks and real-world project submissions.

📌 Now, continuing with your application: could you please provide your full name?

You: My name is Pranav Bhargav
Bot: Thank you, Pranav Bhargav! Next, please provide your email address.

You: my email is student@example.com
Bot: Great! Your email student@example.com is recorded.

Now, what is your field of study or degree program? (e.g., Computer Science, AI, Data Science)

You: Artificial Intelligence and Data Science
Bot: Perfect! Field of study recorded as 'Artificial Intelligence & Machine Learning'.

Lastly, what is your programming / technical experience level? (e.g., Beginner, Intermediate, or Advanced)

You: Intermediate level
Bot: 🎉 Congratulations, Pranav Bhargav! Your internship registration is confirmed!

📋 Registration Summary:
• Name: Pranav Bhargav
• Email: student@example.com
• Field: Artificial Intelligence & Machine Learning
• Experience: Intermediate (1-2 yrs)
• Timestamp: 2026-09-19 01:38:01

Your candidate profile has been securely saved to the database. Feel free to ask any other questions or type 'help'.
```

---

## 📋 Evaluation Checklist

- [x] Python 3.10+ implementation
- [x] NLP Preprocessing (Tokenization, Lemmatization, Stopwords)
- [x] Scikit-Learn ML Intent Classification
- [x] Entity Extraction (Name, Email, Field, Experience)
- [x] Input Validation Checks (RFC 5322 Email regex, Name format)
- [x] Dialog Management with state preservation and slot-filling
- [x] JSON Data Persistence (`registrations.json`)
- [x] Interactive FAQ handling & Sentiment Analysis
- [x] Responsive Web Chat Interface (Flask)
- [x] Admin Dashboard & Analytics (`/admin`)
- [x] Comprehensive Report (`REPORT.md`)
- [x] Submission Guide with Blog Post & Video Demo Script (`SUBMISSION_GUIDE.md`)

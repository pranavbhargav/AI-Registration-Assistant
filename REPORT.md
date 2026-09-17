# Project Report: AI Registration Assistant Using NLP

**Task ID:** AI-SS-001  
**Student Code:** DAS010164  
**Project Name:** AI Registration Assistant  
**Date:** September 2026  

---

## 1. Executive Summary
The **AI Registration Assistant** is an intelligent conversational agent developed to automate and enhance the internship registration experience for prospective student applicants. By integrating Natural Language Processing (NLP) techniques, rule-based intent recognition, and entity extraction algorithms, the chatbot guides applicants through an intuitive conversational dialog, extracts critical candidate entities, validates inputs, and records candidate profiles into persistent structured storage.

---

## 2. Project Objectives
- **Automate Registration:** Provide a seamless, automated interface to collect applicant data without human intervention.
- **Implement NLP Fundamentals:** Utilize tokenization, stopword removal, and vocabulary normalization to process unstructured text inputs.
- **Support Intent Classification & Entity Extraction:** Accurately classify user goals (greeting, registration, queries, termination) and extract candidate entities (full name, email address) from natural user queries.
- **Provide Robust Dialog Management:** Maintain stateful interaction loops handling edge cases, unrecognized queries, and multi-step registration sequences.
- **Store Data Reliably:** Maintain a persistent, structured JSON-based datastore (`registrations.json`) for seamless integration with downstream internship evaluation workflows.

---

## 3. Technologies Used & System Architecture

| Technology / Library | Purpose in Project |
| :--- | :--- |
| **Python 3.10+** | Core programming language for application logic and dialog execution |
| **NLTK (Natural Language Toolkit)** | Lexical preprocessing, tokenization (`word_tokenize`), and stopword filtration |
| **Regular Expressions (`re`)** | Pattern-based extraction of named entities (e.g., student name, email addresses) |
| **JSON** | Configuration management (`intents.json`) and data persistence (`registrations.json`) |
| **Scikit-Learn** | NLP and machine learning pipeline dependencies |

### System Architecture Flow:
```
[User Input] 
     │
     ▼
[NLP Preprocessing: Tokenize, Lowercase, Remove Stopwords]
     │
     ├──► [Intent Classification Engine] ──► (Greeting / Help / Bye / Register)
     │                                            │
     └──► [Regex Entity Extraction]                ▼
          (Extracts Name & Email)      [Interactive Registration Flow]
                                                  │
                                                  ▼
                                      [JSON Persistent Storage]
                                      (registrations.json)
```

---

## 4. Key Features Implemented

1. **Greeting & Conversational Entry:**
   - Detects welcoming phrases (`hi`, `hello`, `hey`, `good morning`) and initiates dialogue with helpful contextual prompts.

2. **Modular Intent Recognition:**
   - Intent definitions configured via `intents.json` with fallback defaults in `app.py`.
   - Supports key operational intents: `greeting`, `register`, `help`, `bye`, with fallback to entity resolution.

3. **Information & Entity Extraction:**
   - **Name Extraction:** Uses conversational context parsing (e.g., `my name is [Name]`, `i am [Name]`, `i'm [Name]`) with regex matching.
   - **Email Extraction:** Uses RFC 5322 compliant regex patterns to identify and extract email addresses directly from continuous user input.

4. **Multi-Step Internship Registration Workflow:**
   - Prompts for Name, Email, Field of Study, and Experience Level.
   - Formats user data into a structured record and appends it to `registrations.json`.

5. **Help & Graceful Exit:**
   - Comprehensive assistance guidelines when prompted with `help` or `support`.
   - Graceful session termination upon `bye`, `exit`, or `quit`.

---

## 5. Results & Sample Execution

### Sample Console Transcript:
```text
AI Registration Assistant Started

You: Hello!
Bot: Hello! Welcome to Internship Registration.

You: My name is Pranav Bhargav
Bot: Nice to meet you Pranav Bhargav

You: My contact email is student@example.com
Bot: Email detected -> student@example.com

You: help
Bot: Type 'register' to begin registration.

You: register

--- Internship Registration ---
Enter Name: Pranav Bhargav
Enter Email: student@example.com
Field of Study: Computer Science & Artificial Intelligence
Experience Level: Intermediate

Registration Successful!
{
    "name": "Pranav Bhargav",
    "email": "student@example.com",
    "field": "Computer Science & Artificial Intelligence",
    "experience": "Intermediate"
}

You: bye
Bot: Goodbye!
```

### Generated `registrations.json` Structure:
```json
[
    {
        "name": "Pranav Bhargav",
        "email": "student@example.com",
        "field": "Computer Science & Artificial Intelligence",
        "experience": "Intermediate"
    }
]
```

---

## 6. Screenshots Checklist for Submission
To complete internship submission criteria, capture screenshots of the following phases:
1. **Program Start:** Chatbot startup banner in terminal.
2. **Greeting Response:** Bot acknowledging greeting inputs.
3. **Registration Process:** Active data entry for Name, Email, Field, Experience.
4. **Registration Success:** Formatted confirmation payload displayed on console.
5. **registrations.json File:** The saved records viewed in code editor or terminal.

---

## 7. Conclusion
The **AI Registration Assistant** successfully meets all specifications outlined in Task **AI-SS-001**. The chatbot demonstrates effective practical implementation of NLP preprocessing, intent classification, pattern-based entity extraction, state-managed conversational workflows, and JSON data persistence. The solution provides a scalable foundation for modern conversational interfaces in academic and enterprise student onboarding.

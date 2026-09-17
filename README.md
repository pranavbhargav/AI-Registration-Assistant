# AI Registration Assistant

Student Code: DAS010164

## Overview
An intelligent conversational chatbot built using Python and Natural Language Processing (NLP) techniques to streamline and automate the student internship registration workflow.

## Features
- **Greeting System:** Welcomes students and initiates the conversational flow.
- **Intent Recognition:** Identifies user intents (`greeting`, `register`, `help`, `bye`) using keyword pattern matching and structured intents definition.
- **Entity Extraction:** Extracts student entities such as full names and email addresses using regular expressions.
- **Dialog Management:** State-driven conversation management guiding the user through interactive prompts.
- **Registration Workflow:** Interactive collection of Name, Email, Field of Study, and Experience Level.
- **JSON Data Storage:** Persistently stores registration records in `registrations.json`.
- **NLP Preprocessing:** Text lowercasing, tokenization, alphanumeric filtering, and stopword removal with NLTK.

## Project Structure
```text
AI-Registration-Assistant/
│
├── app.py                  # Main chatbot application logic & dialog manager
├── registrations.json      # Persistent storage for registered student records
├── requirements.txt        # Python package dependencies (nltk, scikit-learn)
├── README.md               # Project documentation & instructions
├── intents.json            # Structured dataset of conversational intents
└── REPORT.md               # 1–2 page comprehensive technical project report
```

## Installation

Ensure Python is installed on your system, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Assistant

Launch the chatbot in your terminal:

```bash
python app.py
```

## Example Interaction
```text
AI Registration Assistant Started

You: Hello!
Bot: Hello! Welcome to Internship Registration.

You: help
Bot: Type 'register' to begin registration.

You: register

--- Internship Registration ---
Enter Name: Pranav Bhargav
Enter Email: pranav@example.com
Field of Study: Computer Science & AI
Experience Level: Intermediate

Registration Successful!
{
    "name": "Pranav Bhargav",
    "email": "pranav@example.com",
    "field": "Computer Science & AI",
    "experience": "Intermediate"
}

You: bye
Bot: Goodbye!
```

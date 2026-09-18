"""
AI Registration Assistant
Task ID: AI-SS-001 | Student Code: DAS010164
Free Online AI & Data Science Internship
"""

import os
import re
import json
import random
from datetime import datetime

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Safely verify and download required NLTK resources
for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass


class RegistrationAssistant:
    """
    Intelligent Conversational Chatbot for Internship Registration.
    Features:
    - NLP Preprocessing (Tokenization, Lemmatization, Stopword Filtering)
    - Hybrid Intent Classification (Scikit-Learn ML Model + Heuristic Matching)
    - Contextual Entity Extraction (Name, Email, Field, Experience)
    - Strict Input Validation & Normalization
    - Stateful Dialog Management (Finite State Machine with Slot Filling)
    - Sentiment Analysis & Empathetic Adaptation
    - FAQ Knowledge Retrieval
    - Persistent JSON Data Storage & Analytics Logging
    """

    def __init__(self, intents_file="intents.json", registrations_file="registrations.json", logs_file="chat_logs.json"):
        self.intents_file = intents_file
        self.registrations_file = registrations_file
        self.logs_file = logs_file

        # Initialize NLP tools
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = set()

        # Load intents and compile training dataset
        self.intents = self._load_intents()

        # Train ML intent classifier
        self.vectorizer = None
        self.classifier = None
        self._train_ml_classifier()

        # Multi-session state management
        self.sessions = {}

    def _load_intents(self):
        """Loads intents from JSON file with a comprehensive default fallback."""
        default_intents = {
            "greeting": {
                "patterns": ["hi", "hello", "hey", "good morning", "good evening", "namaste", "hola", "greetings"],
                "responses": ["Hello! Welcome to the AI & Data Science Internship Registration Assistant. How can I help you today?"]
            },
            "register": {
                "patterns": ["register", "apply", "join", "sign up", "enroll", "i want to apply", "internship registration"],
                "responses": ["Great! Let's get you registered for the AI & Data Science Internship. What is your full name?"]
            },
            "help": {
                "patterns": ["help", "guide", "support", "what can you do", "commands"],
                "responses": ["I can assist you with:\n1. 'register' - Start your internship application\n2. 'duration', 'stipend', 'certificate', 'skills' - Ask FAQs\n3. 'status' - Check application status\n4. 'exit' - End conversation"]
            },
            "faq_duration": {
                "patterns": ["how long is the internship", "duration", "timeline", "how many weeks"],
                "responses": ["The internship spans a flexible 1 to 4 weeks, organized into self-paced project tasks and milestone deliverables."]
            },
            "faq_certificate": {
                "patterns": ["will i get a certificate", "certificate", "certification", "completion letter"],
                "responses": ["Yes! A verified Internship Completion Certificate is awarded upon successful evaluation of your project submission."]
            },
            "faq_stipend": {
                "patterns": ["is it paid", "stipend", "fees", "cost", "free"],
                "responses": ["This is a 100% Free Virtual Learning Internship aimed at skill acquisition and portfolio building with zero registration charges."]
            },
            "faq_skills": {
                "patterns": ["skills required", "prerequisites", "python needed", "technologies"],
                "responses": ["The core technologies used are Python, NLP (NLTK/spaCy), Machine Learning (Scikit-Learn), and Web/API integration."]
            },
            "faq_eligibility": {
                "patterns": ["who can apply", "eligibility", "can college students apply"],
                "responses": ["Undergraduate and postgraduate students, freshers, and AI enthusiasts eager to build hands-on data science projects are welcome!"]
            },
            "bye": {
                "patterns": ["bye", "exit", "quit", "goodbye", "see you"],
                "responses": ["Thank you for using the AI Registration Assistant. Best of luck with your internship! Goodbye!"]
            }
        }

        if os.path.exists(self.intents_file):
            try:
                with open(self.intents_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        for k, v in loaded.items():
                            if isinstance(v, list):
                                default_intents[k] = {"patterns": v, "responses": default_intents.get(k, {}).get("responses", ["Received."])}
                            elif isinstance(v, dict):
                                default_intents[k] = v
            except Exception as e:
                print(f"[Warning] Error loading {self.intents_file}: {e}")

        return default_intents

    def preprocess_text(self, text):
        """Tokenization, lowercasing, punctuation stripping, stopword removal, and lemmatization."""
        text = text.lower()
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = re.findall(r'\b\w+\b', text)

        cleaned_tokens = []
        for token in tokens:
            if token.isalnum() and token not in self.stop_words:
                try:
                    lemma = self.lemmatizer.lemmatize(token)
                except Exception:
                    lemma = token
                cleaned_tokens.append(lemma)
        return cleaned_tokens

    def _train_ml_classifier(self):
        """Trains a Scikit-Learn TF-IDF + LogisticRegression model on the intents dataset."""
        corpus = []
        labels = []

        for tag, data in self.intents.items():
            patterns = data.get("patterns", [])
            for pattern in patterns:
                tokens = self.preprocess_text(pattern)
                clean_sentence = " ".join(tokens)
                if clean_sentence.strip():
                    corpus.append(clean_sentence)
                    labels.append(tag)

        if len(set(labels)) > 1 and len(corpus) >= 2:
            try:
                self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
                X = self.vectorizer.fit_transform(corpus)
                self.classifier = LogisticRegression(max_iter=300, random_state=42)
                self.classifier.fit(X, labels)
            except Exception as e:
                print(f"[Warning] ML training failed, defaulting to rule-based intent recognition: {e}")
                self.vectorizer = None
                self.classifier = None

    def classify_intent(self, text):
        """
        Hybrid Intent Classification:
        Combines pattern heuristics for exact matches with ML-based TF-IDF classification.
        Returns: (intent_tag, confidence_score)
        """
        text_lower = text.lower().strip()

        # Fast heuristic keyword / phrase check
        for tag, data in self.intents.items():
            for pattern in data.get("patterns", []):
                p_lower = pattern.lower().strip()
                if p_lower == text_lower or (len(p_lower) > 3 and p_lower in text_lower):
                    return tag, 1.0

        # ML classifier evaluation
        if self.vectorizer and self.classifier:
            try:
                tokens = self.preprocess_text(text)
                if tokens:
                    processed_text = " ".join(tokens)
                    X_input = self.vectorizer.transform([processed_text])
                    probs = self.classifier.predict_proba(X_input)[0]
                    max_prob = max(probs)
                    predicted_tag = self.classifier.classes_[probs.argmax()]
                    if max_prob >= 0.28:
                        return predicted_tag, float(round(max_prob, 3))
            except Exception:
                pass

        return "unknown", 0.0

    def analyze_sentiment(self, text):
        """
        Lexicon-based sentiment scoring.
        Returns: 'positive', 'negative', or 'neutral'
        """
        positive_words = {
            "good", "great", "excellent", "awesome", "perfect", "happy", "thank",
            "thanks", "cool", "nice", "helpful", "love", "wonderful", "excited"
        }
        negative_words = {
            "bad", "terrible", "horrible", "worst", "confused", "frustrated",
            "hate", "problem", "difficult", "hard", "stuck", "error", "useless", "poor"
        }

        tokens = set(re.findall(r'\b\w+\b', text.lower()))
        pos_hits = len(tokens.intersection(positive_words))
        neg_hits = len(tokens.intersection(negative_words))

        if pos_hits > neg_hits:
            return "positive"
        elif neg_hits > pos_hits:
            return "negative"
        return "neutral"

    # --- Entity Extraction & Validation Methods ---

    def extract_name(self, text):
        """Extracts candidate's full name using regex and conversational context."""
        # Check patterns like "My name is John Doe", "I am John Doe", "I'm John Doe"
        match = re.search(r"(?:my name is|i am|i'm|call me|this is)\s+([a-zA-Z\s\.\-]{2,40})", text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if self.validate_name(candidate):
                return candidate.title()

        # If text is already a clean 1-4 word alphabetic string
        clean_text = text.strip()
        if re.match(r"^[a-zA-Z\s\.\-]{2,40}$", clean_text) and not any(kw in clean_text.lower() for kw in ["hi", "hello", "register", "help", "duration", "stipend"]):
            words = clean_text.split()
            if 1 <= len(words) <= 4:
                return clean_text.title()
        return None

    def validate_name(self, name):
        """Validates that a name contains valid alphabetic characters and realistic length."""
        if not name or len(name) < 2 or len(name) > 50:
            return False
        # Disallow pure numbers or symbols
        if not re.match(r"^[a-zA-Z\s\.\-']+$", name):
            return False
        # Disallow obvious bot command words
        blacklist = {"register", "internship", "help", "duration", "certificate", "stipend", "exit", "quit"}
        if name.lower() in blacklist:
            return False
        return True

    def extract_email(self, text):
        """Extracts email address using standard RFC 5322 regex pattern."""
        match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        if match:
            candidate = match.group().lower().strip()
            if self.validate_email(candidate):
                return candidate
        return None

    def validate_email(self, email):
        """Validates standard email formatting and common domains."""
        if not email or len(email) > 100:
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def extract_field(self, text):
        """Matches candidate field of study against standard engineering and science tracks."""
        fields_catalog = [
            ("Computer Science & Engineering", ["computer science", "cse", "cs", "computer"]),
            ("Artificial Intelligence & Machine Learning", ["ai", "ml", "aiml", "artificial intelligence", "machine learning"]),
            ("Data Science & Analytics", ["data science", "data analytics", "data analysis", "big data"]),
            ("Information Technology", ["information technology", "it"]),
            ("Electronics & Communication", ["electronics", "ece", "electrical", "eee"]),
            ("Software Engineering", ["software", "software engineering", "swe"]),
            ("Mechanical & Civil Engineering", ["mechanical", "civil", "robotics"])
        ]
        text_lower = text.lower()
        for formal_name, aliases in fields_catalog:
            for alias in aliases:
                if re.search(rf"\b{re.escape(alias)}\b", text_lower):
                    return formal_name

        # If user typed a custom field with realistic length
        clean = text.strip()
        if 2 <= len(clean) <= 60 and not re.search(r"[<>{}\$]", clean):
            return clean.title()
        return None

    def extract_experience(self, text):
        """Maps user experience level to Beginner, Intermediate, or Advanced."""
        text_lower = text.lower()
        if any(w in text_lower for w in ["beginner", "fresher", "newbie", "basic", "learning", "starter", "novice", "0"]):
            return "Beginner (0-1 yrs)"
        elif any(w in text_lower for w in ["intermediate", "moderate", "medium", "some experience", "1-2", "2 years"]):
            return "Intermediate (1-2 yrs)"
        elif any(w in text_lower for w in ["advanced", "expert", "senior", "pro", "proficient", "3+"]):
            return "Advanced (2+ yrs)"
        
        # Clean fallback text
        clean = text.strip()
        if 2 <= len(clean) <= 40:
            return clean.capitalize()
        return "Beginner (0-1 yrs)"

    # --- Dialog State Management ---

    def get_session(self, session_id="default"):
        """Retrieves or initializes session state for a given user session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "state": "IDLE",  # IDLE, AWAITING_NAME, AWAITING_EMAIL, AWAITING_FIELD, AWAITING_EXPERIENCE, CONFIRMATION
                "data": {
                    "name": None,
                    "email": None,
                    "field": None,
                    "experience": None,
                    "registered_at": None
                }
            }
        return self.sessions[session_id]

    def reset_session(self, session_id="default"):
        """Resets session data and returns state to IDLE."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        return self.get_session(session_id)

    def process_message(self, user_input, session_id="default"):
        """
        Core Conversational Engine:
        Processes user turn, manages Finite State Machine transitions,
        supports mid-flow FAQ queries, validates inputs, and records registrations.
        """
        user_input = user_input.strip()
        session = self.get_session(session_id)
        current_state = session["state"]
        user_data = session["data"]

        sentiment = self.analyze_sentiment(user_input)
        intent, confidence = self.classify_intent(user_input)

        response = ""
        is_completed = False

        # Check for immediate exit / cancellation request
        if intent == "bye" or user_input.lower() in ["exit", "quit", "cancel"]:
            self.reset_session(session_id)
            response = "Conversation session ended. Thank you for visiting the AI Registration Assistant! Have a great day!"
            self.log_interaction(session_id, user_input, response, "bye", confidence, sentiment)
            return {
                "response": response,
                "intent": "bye",
                "confidence": confidence,
                "sentiment": sentiment,
                "state": "IDLE",
                "user_data": user_data,
                "is_completed": False
            }

        # Check for mid-flow FAQ interruption
        if intent.startswith("faq_") and current_state != "IDLE":
            faq_reply = random.choice(self.intents[intent]["responses"])
            resume_prompt = {
                "AWAITING_NAME": "Now, continuing with your application: could you please provide your full name?",
                "AWAITING_EMAIL": f"Now, continuing with your application: what is your email address, {user_data.get('name', 'candidate')}?",
                "AWAITING_FIELD": "Now, continuing with your application: what is your field or branch of study?",
                "AWAITING_EXPERIENCE": "Now, continuing with your application: what is your programming experience level?"
            }.get(current_state, "Let's continue your registration.")
            response = f"{faq_reply}\n\n📌 {resume_prompt}"
            self.log_interaction(session_id, user_input, response, intent, confidence, sentiment)
            return {
                "response": response,
                "intent": intent,
                "confidence": confidence,
                "sentiment": sentiment,
                "state": current_state,
                "user_data": user_data,
                "is_completed": False
            }

        # --- State Machine Transitions ---

        if current_state == "IDLE":
            # Check for slot-filling (user provided name and/or email in initial prompt)
            extracted_name = self.extract_name(user_input)
            extracted_email = self.extract_email(user_input)

            if intent == "register" or "register" in user_input.lower() or "apply" in user_input.lower():
                if extracted_name:
                    user_data["name"] = extracted_name
                if extracted_email:
                    user_data["email"] = extracted_email

                if not user_data["name"]:
                    session["state"] = "AWAITING_NAME"
                    response = "Awesome! I'll guide you step-by-step through the internship registration. First, what is your full name?"
                elif not user_data["email"]:
                    session["state"] = "AWAITING_EMAIL"
                    response = f"Nice to meet you, {user_data['name']}! Next, please provide your email address."
                else:
                    session["state"] = "AWAITING_FIELD"
                    response = f"Got it, {user_data['name']} ({user_data['email']})! What is your current field of study or engineering branch?"

            elif intent == "greeting":
                empathy = "Glad to connect with you! " if sentiment == "positive" else ""
                greeting_res = random.choice(self.intents["greeting"]["responses"])
                response = f"{empathy}{greeting_res}\n\nType 'register' to apply, or ask any questions about the internship."

            elif intent == "help":
                response = random.choice(self.intents["help"]["responses"])

            elif intent.startswith("faq_"):
                response = random.choice(self.intents[intent]["responses"]) + "\n\nWould you like to start your registration now? Type 'register' to proceed."

            elif intent == "status":
                if extracted_email:
                    existing = self.find_registration_by_email(extracted_email)
                    if existing:
                        response = f"✅ Registration Record Found!\nName: {existing['name']}\nEmail: {existing['email']}\nField: {existing['field']}\nExperience: {existing['experience']}\nDate: {existing.get('registered_at', 'N/A')}"
                    else:
                        response = f"No registration found for {extracted_email}. Would you like to register now? Type 'register' to begin."
                else:
                    response = "To check your application status, please provide your registered email address (e.g. 'status for student@example.com')."

            elif intent == "sentiment_positive":
                response = random.choice(self.intents["sentiment_positive"]["responses"])

            elif intent == "sentiment_negative":
                response = random.choice(self.intents["sentiment_negative"]["responses"])

            else:
                # If user typed their name or email directly
                if extracted_name:
                    user_data["name"] = extracted_name
                    session["state"] = "AWAITING_EMAIL"
                    response = f"Nice to meet you, {extracted_name}! Let's register you for the internship. What is your email address?"
                elif extracted_email:
                    user_data["email"] = extracted_email
                    session["state"] = "AWAITING_NAME"
                    response = f"Email recorded ({extracted_email}). What is your full name?"
                else:
                    response = "I didn't quite catch that. You can type 'register' to apply for the internship, or ask questions like 'duration', 'stipend', or 'certificate'. How can I assist you?"

        elif current_state == "AWAITING_NAME":
            name = self.extract_name(user_input)
            if name and self.validate_name(name):
                user_data["name"] = name
                session["state"] = "AWAITING_EMAIL"
                response = f"Thank you, {name}! Next, please provide your email address."
            else:
                response = "Please provide a valid full name (alphabetic characters only, e.g., 'Pranav Bhargav')."

        elif current_state == "AWAITING_EMAIL":
            email = self.extract_email(user_input)
            if email and self.validate_email(email):
                user_data["email"] = email
                session["state"] = "AWAITING_FIELD"
                response = f"Great! Your email {email} is recorded.\n\nNow, what is your field of study or degree program? (e.g., Computer Science, AI, Data Science)"
            else:
                response = "That doesn't look like a valid email address. Please provide a valid email format like 'student@example.com'."

        elif current_state == "AWAITING_FIELD":
            field = self.extract_field(user_input)
            if field:
                user_data["field"] = field
                session["state"] = "AWAITING_EXPERIENCE"
                response = f"Perfect! Field of study recorded as '{field}'.\n\nLastly, what is your programming / technical experience level? (e.g., Beginner, Intermediate, or Advanced)"
            else:
                response = "Please enter a valid field of study (e.g., Computer Science, Data Science, Artificial Intelligence, IT)."

        elif current_state == "AWAITING_EXPERIENCE":
            experience = self.extract_experience(user_input)
            user_data["experience"] = experience
            user_data["registered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save persistent record
            self.save_registration(user_data)
            is_completed = True
            session["state"] = "IDLE"

            response = (
                f"🎉 Congratulations, {user_data['name']}! Your internship registration is confirmed!\n\n"
                f"📋 Registration Summary:\n"
                f"• Name: {user_data['name']}\n"
                f"• Email: {user_data['email']}\n"
                f"• Field: {user_data['field']}\n"
                f"• Experience: {user_data['experience']}\n"
                f"• Timestamp: {user_data['registered_at']}\n\n"
                f"Your candidate profile has been securely saved to the database. Feel free to ask any other questions or type 'help'."
            )

        # Log conversation turn for analytics
        self.log_interaction(session_id, user_input, response, intent, confidence, sentiment)

        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "sentiment": sentiment,
            "state": session["state"],
            "user_data": user_data,
            "is_completed": is_completed
        }

    def save_registration(self, student_data):
        """Appends registration record to registrations.json."""
        records = []
        if os.path.exists(self.registrations_file):
            try:
                with open(self.registrations_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        records = content
            except Exception:
                records = []

        # Avoid exact duplicate email spam by updating or appending
        records = [r for r in records if r.get("email") != student_data.get("email")]
        records.append(student_data)

        try:
            with open(self.registrations_file, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save registration: {e}")

    def find_registration_by_email(self, email):
        """Looks up a registered student by email address."""
        if os.path.exists(self.registrations_file):
            try:
                with open(self.registrations_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    for r in records:
                        if r.get("email", "").lower() == email.lower():
                            return r
            except Exception:
                pass
        return None

    def log_interaction(self, session_id, user_input, bot_response, intent, confidence, sentiment):
        """Logs chat session metrics to chat_logs.json for analytics and admin reporting."""
        log_entry = {
            "session_id": session_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_input": user_input,
            "bot_response": bot_response,
            "intent": intent,
            "confidence": confidence,
            "sentiment": sentiment
        }
        logs = []
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        logs = loaded
            except Exception:
                logs = []

        logs.append(log_entry)
        try:
            with open(self.logs_file, "w", encoding="utf-8") as f:
                json.dump(logs[-1000:], f, indent=2)  # Keep recent 1000 logs
        except Exception:
            pass

    def get_analytics(self):
        """Calculates dashboard metrics: total candidates, field breakdown, sentiment, recent logs."""
        registrations = []
        if os.path.exists(self.registrations_file):
            try:
                with open(self.registrations_file, "r", encoding="utf-8") as f:
                    registrations = json.load(f)
            except Exception:
                registrations = []

        logs = []
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except Exception:
                logs = []

        # Field distributions
        field_counts = {}
        exp_counts = {}
        for r in registrations:
            f = r.get("field", "Other")
            e = r.get("experience", "Not Specified")
            field_counts[f] = field_counts.get(f, 0) + 1
            exp_counts[e] = exp_counts.get(e, 0) + 1

        # Sentiment distributions
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for log in logs:
            s = log.get("sentiment", "neutral")
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1

        return {
            "total_registrations": len(registrations),
            "total_messages": len(logs),
            "field_distribution": field_counts,
            "experience_distribution": exp_counts,
            "sentiment_distribution": sentiment_counts,
            "recent_registrations": registrations[-10:],
            "recent_logs": logs[-10:]
        }

    def run(self):
        """Interactive Terminal Conversational Interface."""
        print("=" * 65)
        print("🤖 AI REGISTRATION ASSISTANT - VIRTUAL INTERNSHIP ADVISOR")
        print("Task ID: AI-SS-001 | Student Code: DAS010164")
        print("=" * 65)
        print("Type 'register' to apply, ask any FAQ questions, or type 'exit' to quit.\n")

        session_id = "cli_user"
        while True:
            try:
                user_msg = input("\nYou: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nBot: Goodbye!")
                break

            if not user_msg:
                continue

            result = self.process_message(user_msg, session_id=session_id)
            print(f"\nBot: {result['response']}")

            if user_msg.lower() in ["exit", "quit", "bye"] and result["intent"] == "bye":
                break


if __name__ == "__main__":
    assistant = RegistrationAssistant()
    assistant.run()

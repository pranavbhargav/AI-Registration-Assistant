import json
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure required NLTK resources are available
for resource in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass


class RegistrationAssistant:

    def __init__(self, intents_file="intents.json"):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = set()

        # Default base intents
        self.intents = {
            "greeting": ["hi", "hello", "hey"],
            "register": ["register", "apply", "join"],
            "help": ["help", "guide", "support"],
            "bye": ["bye", "exit", "quit"]
        }

        # Load external intents if intents.json exists
        if os.path.exists(intents_file):
            try:
                with open(intents_file, "r", encoding="utf-8") as f:
                    loaded_intents = json.load(f)
                    if isinstance(loaded_intents, dict):
                        self.intents.update(loaded_intents)
            except Exception as e:
                print(f"[Warning] Could not load {intents_file}: {e}")

        self.user_data = {}

    def preprocess(self, text):
        text = text.lower()
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = re.findall(r'\b\w+\b', text)
        tokens = [w for w in tokens if w.isalnum()]
        tokens = [w for w in tokens if w not in self.stop_words]
        return tokens

    def classify_intent(self, text):
        text = text.lower()

        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in text:
                    return intent

        return "unknown"

    def extract_name(self, text):
        match = re.search(r"(?:my name is|i am|i'm)\s+([a-zA-Z ]+)", text, re.I)
        if match:
            return match.group(1).strip()
        return None

    def extract_email(self, text):
        match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            text
        )
        if match:
            return match.group()
        return None

    def save_registration(self):
        try:
            with open("registrations.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

        if not isinstance(data, list):
            data = []

        data.append(self.user_data)

        with open("registrations.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def register_user(self):

        print("\n--- Internship Registration ---")

        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        field = input("Field of Study: ").strip()
        experience = input("Experience Level: ").strip()

        self.user_data = {
            "name": name,
            "email": email,
            "field": field,
            "experience": experience
        }

        self.save_registration()

        print("\nRegistration Successful!")
        print(json.dumps(self.user_data, indent=4))

    def run(self):

        print("AI Registration Assistant Started")

        while True:

            user = input("\nYou: ")

            intent = self.classify_intent(user)

            if intent == "greeting":
                print("Bot: Hello! Welcome to Internship Registration.")

            elif intent == "register":
                self.register_user()

            elif intent == "help":
                print("Bot: Type 'register' to begin registration.")

            elif intent == "bye":
                print("Bot: Goodbye!")
                break

            else:
                name = self.extract_name(user)
                email = self.extract_email(user)

                if name:
                    print(f"Bot: Nice to meet you {name}")

                elif email:
                    print(f"Bot: Email detected -> {email}")

                else:
                    print("Bot: I didn't understand that.")


if __name__ == "__main__":
    bot = RegistrationAssistant()
    bot.run()

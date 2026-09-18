"""
Unit & Integration Tests for AI Registration Assistant
Tests NLP preprocessing, ML classification, entity validation, dialog state machine, and persistence.
"""

import os
import json
from app import RegistrationAssistant

def test_nlp_and_ml():
    bot = RegistrationAssistant()
    print("Testing NLP & ML Intent Classifier...")
    
    # Check preprocessing
    tokens = bot.preprocess_text("I am registering for the artificial intelligence internship")
    assert "register" in tokens or "registering" in tokens or "internship" in tokens
    
    # Test intent classification
    intent, conf = bot.classify_intent("hello there")
    assert intent == "greeting"
    print(f"  [OK] Greeting recognized: {intent} (conf: {conf})")
    
    intent, conf = bot.classify_intent("how long is the internship?")
    assert intent == "faq_duration"
    print(f"  [OK] FAQ Duration recognized: {intent} (conf: {conf})")
    
    intent, conf = bot.classify_intent("will I get a certificate?")
    assert intent == "faq_certificate"
    print(f"  [OK] FAQ Certificate recognized: {intent} (conf: {conf})")

def test_entity_validation():
    bot = RegistrationAssistant()
    print("\nTesting Entity Extraction & Validation...")
    
    # Email
    assert bot.validate_email("student@domain.com") == True
    assert bot.validate_email("invalid-email") == False
    extracted_email = bot.extract_email("Please contact me at test.user@gmail.com for details")
    assert extracted_email == "test.user@gmail.com"
    print("  [OK] Email validation passed.")
    
    # Name
    assert bot.validate_name("Pranav Bhargav") == True
    assert bot.validate_name("12345") == False
    assert bot.validate_name("a") == False
    extracted_name = bot.extract_name("My name is Pranav Bhargav")
    assert extracted_name == "Pranav Bhargav"
    print("  [OK] Name validation passed.")

def test_conversational_dialog_flow():
    bot = RegistrationAssistant(registrations_file="test_registrations.json", logs_file="test_logs.json")
    session_id = "test_user_1"
    print("\nTesting Stateful Conversational Flow with Mid-Flow FAQ Interruption...")
    
    # 1. Start registration
    r1 = bot.process_message("I want to register", session_id)
    assert r1["state"] == "AWAITING_NAME"
    print(f"  Turn 1 (Start): State -> {r1['state']}")
    
    # 2. User interrupts with FAQ
    r2 = bot.process_message("Wait, how long is the internship?", session_id)
    assert r2["state"] == "AWAITING_NAME"
    assert "flexible" in r2["response"].lower() and "week" in r2["response"].lower()
    print(f"  Turn 2 (FAQ Interruption Handled): Response -> {r2['response'][:60]}...")
    
    # 3. Provide name
    r3 = bot.process_message("My name is John Doe", session_id)
    assert r3["state"] == "AWAITING_EMAIL"
    print(f"  Turn 3 (Name): State -> {r3['state']}")
    
    # 4. Provide invalid email
    r4 = bot.process_message("not_an_email", session_id)
    assert r4["state"] == "AWAITING_EMAIL"
    assert "valid email" in r4["response"].lower()
    print(f"  Turn 4 (Invalid Email Handled): State -> {r4['state']}")
    
    # 5. Provide valid email
    r5 = bot.process_message("john.doe@university.edu", session_id)
    assert r5["state"] == "AWAITING_FIELD"
    print(f"  Turn 5 (Valid Email): State -> {r5['state']}")
    
    # 6. Provide field of study
    r6 = bot.process_message("Data Science", session_id)
    assert r6["state"] == "AWAITING_EXPERIENCE"
    print(f"  Turn 6 (Field): State -> {r6['state']}")
    
    # 7. Provide experience
    r7 = bot.process_message("Intermediate level", session_id)
    assert r7["is_completed"] == True
    assert r7["state"] == "IDLE"
    print(f"  Turn 7 (Confirmation): Registration Completed successfully!")
    
    # Verify file saved
    assert os.path.exists("test_registrations.json")
    with open("test_registrations.json", "r") as f:
        records = json.load(f)
        assert len(records) > 0
        assert records[-1]["name"] == "John Doe"
        assert records[-1]["email"] == "john.doe@university.edu"
        print(f"  [OK] Saved Record: {records[-1]}")
    
    # Cleanup test files
    if os.path.exists("test_registrations.json"):
        os.remove("test_registrations.json")
    if os.path.exists("test_logs.json"):
        os.remove("test_logs.json")

def test_web_routes():
    from web_app import app
    print("\nTesting Flask Web Server Endpoints & Admin Dashboard...")
    client = app.test_client()
    
    assert client.get("/").status_code == 200
    print("  [OK] GET / (Chat UI) -> 200")
    
    r_chat = client.post("/api/chat", json={"message": "hello", "session_id": "test_web"})
    assert r_chat.status_code == 200
    print("  [OK] POST /api/chat -> 200")
    
    assert client.get("/admin").status_code == 200
    print("  [OK] GET /admin (Admin Dashboard) -> 200")
    
    assert client.get("/api/analytics").status_code == 200
    print("  [OK] GET /api/analytics -> 200")
    
    r_csv = client.get("/api/export-csv")
    assert r_csv.status_code == 200
    print("  [OK] GET /api/export-csv -> 200 (CSV)")

if __name__ == "__main__":
    test_nlp_and_ml()
    test_entity_validation()
    test_conversational_dialog_flow()
    test_web_routes()
    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

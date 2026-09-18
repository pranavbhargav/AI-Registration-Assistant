"""
Flask Web Application & Admin Dashboard
AI Registration Assistant
Task ID: AI-SS-001 | Student Code: DAS010164
"""

import os
import csv
import io
from flask import Flask, render_template, request, jsonify, Response
from app import RegistrationAssistant

app = Flask(__name__)
bot = RegistrationAssistant()


@app.route("/")
def home():
    """Renders the conversational web chat interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """API endpoint for asynchronous chat messaging."""
    payload = request.get_json(silent=True) or {}
    user_msg = payload.get("message", "").strip()
    session_id = payload.get("session_id", "web_session_1")

    if not user_msg:
        return jsonify({"error": "Empty message received"}), 400

    result = bot.process_message(user_msg, session_id=session_id)
    return jsonify(result)


@app.route("/api/reset", methods=["POST"])
def reset():
    """Resets user chat session state."""
    payload = request.get_json(silent=True) or {}
    session_id = payload.get("session_id", "web_session_1")
    bot.reset_session(session_id)
    return jsonify({"status": "reset", "message": "Session restarted successfully."})


@app.route("/admin")
def admin_dashboard():
    """Renders the Admin Dashboard with registration and analytics statistics."""
    analytics = bot.get_analytics()
    return render_template("admin.html", analytics=analytics)


@app.route("/api/analytics")
def api_analytics():
    """Returns real-time analytics data in JSON format."""
    return jsonify(bot.get_analytics())


@app.route("/api/export-csv")
def export_csv():
    """Exports all registered student applications as a CSV file."""
    analytics = bot.get_analytics()
    registrations = analytics.get("recent_registrations", [])
    
    # Reload full registrations list
    if os.path.exists(bot.registrations_file):
        try:
            import json
            with open(bot.registrations_file, "r", encoding="utf-8") as f:
                registrations = json.load(f)
        except Exception:
            pass

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Email", "Field of Study", "Experience Level", "Registration Date"])
    for r in registrations:
        writer.writerow([
            r.get("name", ""),
            r.get("email", ""),
            r.get("field", ""),
            r.get("experience", ""),
            r.get("registered_at", "")
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=internship_registrations.csv"}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting AI Registration Assistant Web App on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

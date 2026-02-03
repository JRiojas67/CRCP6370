#!/usr/bin/env python3
"""
Flask server to serve the chatbot web UI (index.html) and provide /api/chat.
Run: python3 server.py
Then open http://127.0.0.1:5500 in your browser.
"""

import os
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory

# Load .env before importing chatbot (so API keys are available)
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        pass

from chatbot_ai import AIChatbot, CLAUDE_AVAILABLE, OPENAI_AVAILABLE

app = Flask(__name__, static_folder=None)


@app.after_request
def add_cors(resp):
    """Allow frontend from file:// or other origins to call /api/chat."""
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "OPTIONS, POST"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Max-Age"] = "86400"
    return resp

# One shared chatbot instance (created on first request)
_chatbot = None


def get_chatbot():
    global _chatbot
    if _chatbot is None:
        if not CLAUDE_AVAILABLE and not OPENAI_AVAILABLE:
            raise RuntimeError("No AI SDKs installed. Install: pip install anthropic openai python-dotenv")
        _chatbot = AIChatbot(default_provider="claude", personality="default")
    return _chatbot


@app.route("/")
def index():
    return send_from_directory(Path(__file__).resolve().parent, "index.html")


@app.route("/api/health")
def health():
    """Let the frontend check if the server is running."""
    return jsonify({"ok": True, "message": "Chatbot server is running"})


@app.route("/api/chat", methods=["OPTIONS", "POST"], strict_slashes=False)
def chat():
    if request.method == "OPTIONS":
        resp = app.make_response(("", 204))
        return resp
    try:
        body = request.get_json(force=True, silent=True) or {}
        message = (body.get("message") or "").strip()
        personality = (body.get("personality") or "default").strip() or "default"

        if not message:
            return jsonify({"error": "Message is required"}), 400

        bot = get_chatbot()

        # Update personality for this session without clearing history
        if personality != bot.personality and personality in bot.PERSONALITIES:
            bot.personality = personality
            bot.system_prompt = bot.PERSONALITIES[personality]

        response = bot.get_response(message)
        if response is None or (isinstance(response, str) and not response.strip()):
            response = "No response from the AI. Please check your API keys and try again."
        return jsonify({"response": str(response).strip() or "No response."})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting CRCP6370 Chatbot server…")
    print("Open http://127.0.0.1:5500 in your browser.")
    app.run(host="0.0.0.0", port=5500, debug=True)

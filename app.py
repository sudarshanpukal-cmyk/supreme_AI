from flask import Flask, render_template, request, jsonify
from llm import ask_ollama
from system_control import handle_system_command
from memory import save_memory, memory_context, add_message
import re

app = Flask(__name__)


def detect_memory(message):
    """Detect and save simple personal facts."""

    patterns = [
        r"(?:remember that\s+)?my name is\s+([A-Za-z][A-Za-z ]*)",
        r"(?:please\s+)?remember my name is\s+([A-Za-z][A-Za-z ]*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            name = match.group(1).strip().rstrip(" .!?")
            save_memory(f"My name is {name}", "Personal")
            return f"Got it! I'll remember that your name is {name}."

    return None


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    # Detect and save personal information.
    memory_reply = detect_memory(message)

    if memory_reply:
        add_message("user", message)
        add_message("assistant", memory_reply)
        return jsonify({"reply": memory_reply, "action": "memory"})

    # Handle approved computer commands.
    result = handle_system_command(message)

    if result is not None:
        add_message("user", message)
        add_message("assistant", result.get("reply", ""))
        return jsonify(result)

    try:
        # Retrieve saved memories.
        memories = memory_context()

        # Send the message and memories to Ollama.
        reply = ask_ollama(message, memories)

        add_message("user", message)
        add_message("assistant", reply)

        return jsonify({"reply": reply, "action": "chat"})

    except Exception as exc:
        app.logger.exception("Ollama request failed")

        return jsonify({
            "reply": "I couldn't reach Ollama. Check that Ollama is running and the model is installed.",
            "error": str(exc)
        }), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
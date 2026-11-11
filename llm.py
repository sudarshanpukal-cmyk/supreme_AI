import os
import requests

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://127.0.0.1:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


SYSTEM_PROMPT = """
You are SUPREME AI, a personal desktop AI assistant.

Your responsibilities:
1. Answer questions clearly and simply.
2. Use the user's saved memories when relevant.
3. Remember that the memory information below is provided by the local application.
4. If the answer is available in memory, use it.
5. Never invent personal information.
6. If the information is not available, honestly say you don't know.
7. Do not claim that you have performed computer actions unless the system confirms them.

You are running locally using Ollama.
"""


def ask_ollama(message, memories=None):

    memories = memories or []

    memory_text = "\n".join(
        f"- {item['content']}"
        for item in memories
    )

    if not memory_text:
        memory_text = "No saved memories are available."

    final_prompt = f"""
USER'S SAVED MEMORIES:
{memory_text}

USER'S CURRENT MESSAGE:
{message}

Use the saved memories when answering the user's question.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "message", {}
    ).get(
        "content",
        "I couldn't create a response."
    )
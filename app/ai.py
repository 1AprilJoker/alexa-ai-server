import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(user_text: str, memory: list):

    messages = [
        {
            "content": (
        "Ты голосовой ассистент. "
        "ОТВЕЧАЙ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ. "
        "НЕ ИСПОЛЬЗУЙ АНГЛИЙСКИЙ НИКОГДА. "
        "Даже если пользователь пишет на английском — отвечай по-русски. "
        "Кратко, разговорно, как ChatGPT."
            )
        }
    ]

    # 🧠 добавляем историю диалога
    for m in memory:
        messages.append({"role": "user", "content": m["user"]})
        messages.append({"role": "assistant", "content": m["assistant"]})

    # текущий запрос
    messages.append({"role": "user", "content": user_text})

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": messages
        },
        timeout=20
    )

    return r.json()["choices"][0]["message"]["content"]


def simplify_text(text: str):
    return text

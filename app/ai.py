import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(prompt: str):

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Ты голосовой ассистент. "
                            "Отвечай ТОЛЬКО на русском языке. "
                            "Очень кратко (1-2 предложения). "
                            "Говори просто, как человек."
                        )
                    },
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )

        return response.json()["choices"][0]["message"]["content"]

    except Exception:
        return "Извини, сейчас есть проблема с ответом"


# упрощение сложных фраз
def simplify_text(text: str):

    replacements = {
        "является": "это",
        "представляет собой": "это",
        "осуществляет": "делает",
        "используется для": "нужно чтобы",
        "основывается на": "работает на",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

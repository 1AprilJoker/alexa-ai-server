import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(prompt: str):

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
                        "You are a voice assistant. "
                        "Always respond in Russian, short and natural."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        },
        timeout=20
    )

    return response.json()["choices"][0]["message"]["content"]

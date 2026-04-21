from fastapi import FastAPI, Request
from app.ai import ask_ai
from app.translit import to_phonetic
from app.alexa import build_response

app = FastAPI()


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/alexa")
async def alexa_webhook(request: Request):

    body = await request.json()

    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except Exception:
        user_text = "hello"

    # 1. AI (Russian)
    ru_answer = ask_ai(user_text)

    # 2. Transliteration for Alexa TTS
    phonetic = to_phonetic(ru_answer)

    # 3. Alexa response
    return build_response(phonetic)

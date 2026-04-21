from fastapi import FastAPI, Request
from app.ai import ask_ai, simplify_text
from app.translit import to_phonetic
from app.alexa import build_response

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/alexa")
async def alexa_webhook(request: Request):

    body = await request.json()

    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except Exception:
        return build_response("Sorry, I did not understand")

    # 1. AI ответ (русский)
    ru = ask_ai(user_text)

    # 2. упрощаем речь
    ru = simplify_text(ru)

    # 3. ограничиваем длину
    ru = ru[:250]

    # 4. транслит
    phonetic = to_phonetic(ru)

    # 5. ответ Alexa
    return build_response(phonetic)

from fastapi import FastAPI, Request
from app.ai import ask_ai, simplify_text
from app.memory import get_memory, save_memory

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/alexa")
async def alexa(req: Request):

    body = await req.json()

    session_id = body["session"]["sessionId"]

    # извлечение текста
    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except:
        user_text = "continue"

    memory = get_memory(session_id)

    # AI
    answer = ask_ai(user_text, memory)
    answer = simplify_text(answer)

    # 🔥 финальная защита от английского
    latin_ratio = sum(c.isascii() and c.isalpha() for c in answer) / max(len(answer), 1)
    if latin_ratio > 0.4:
        answer = "Извини, повтори вопрос"

    save_memory(session_id, user_text, answer)

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": answer
            },
            "shouldEndSession": False
        }
    }

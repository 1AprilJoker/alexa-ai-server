from fastapi import FastAPI, Request
from app.ai import ask_ai, simplify_text
from app.memory import get_memory, save_memory
from app.alexa import build_response

app = FastAPI()


@app.post("/alexa")
async def alexa(req: Request):

    body = await req.json()

    session_id = body["session"]["sessionId"]
    session_new = body["session"]["new"]

    intent = body["request"].get("intent", {}).get("name", "")

    # 🧠 1. LaunchRequest = старт чата
    if session_new:
        return build_response(
            "Hi. I'm ready. Ask me anything."
        )

    # 🧠 2. извлечение текста
    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except:
        user_text = "continue"

    # 🧠 3. memory load
    memory = get_memory(session_id)

    # 🧠 4. AI
    ru = ask_ai(user_text, memory)
    ru = simplify_text(ru)

    # 🧠 5. save memory
    save_memory(session_id, user_text, ru)

    # 🔥 6. НЕ закрываем сессию
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": ru
            },
            "shouldEndSession": False
        }
    }

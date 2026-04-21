from fastapi import FastAPI, Request
from app.ai import ask_ai, simplify_text
from app.memory import get_memory, save_memory

# 🔥 Spotify imports
from app.spotify_api import search_track, play_track
from app.storage import get_token

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


# =========================
# 🔥 ALEXA WEBHOOK
# =========================
@app.post("/alexa")
async def alexa(req: Request):

    body = await req.json()

    session_id = body["session"]["sessionId"]

    intent = body["request"]["intent"]["name"]

    # -------------------------
    # extract user text safely
    # -------------------------
    try:
        user_text = body["request"]["intent"]["slots"]["query"]["value"]
    except:
        user_text = "continue"

    memory = get_memory(session_id)

    # =========================
    # 🎧 SPOTIFY INTENT
    # =========================
    if intent == "PlayMusicIntent":

        token = get_token(session_id)

        if not token:
            answer = "Spotify не подключен"

        else:
            access_token = token["access_token"]

            uri = search_track(user_text, access_token)

            if uri:
                play_track(uri, access_token)
                answer = "Включаю музыку"
            else:
                answer = "Не нашёл подходящую песню"

    # =========================
    # 🤖 AI DEFAULT MODE
    # =========================
    else:

        answer = ask_ai(user_text, memory)
        answer = simplify_text(answer)

        # 🔥 защита от английского
        latin_ratio = sum(c.isascii() and c.isalpha() for c in answer) / max(len(answer), 1)

        if latin_ratio > 0.4:
            answer = "Извини, повтори вопрос"

    # =========================
    # 💾 MEMORY SAVE
    # =========================
    save_memory(session_id, user_text, answer)

    # =========================
    # 📢 ALEXA RESPONSE
    # =========================
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

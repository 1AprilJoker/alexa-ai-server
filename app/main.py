from fastapi import FastAPI, Request
from app.ai import ask_ai, simplify_text
from app.memory import get_memory, save_memory

from app.spotify_api import search_track, play_track
from app.storage import get_token

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/alexa")
async def alexa(req: Request):

    body = await req.json()

    request = body.get("request", {})
    request_type = request.get("type", "")

    # =========================
    # 🔥 SAFE USER ID (CRITICAL FIX)
    # =========================
    session_id = body.get("session", {}).get("user", {}).get("userId", "unknown_user")

    # =========================
    # 🔥 SAFE INTENT PARSING
    # =========================
    intent = None
    if request_type == "IntentRequest":
        intent = request.get("intent", {}).get("name")

    # =========================
    # 🔥 SAFE SLOT EXTRACTION
    # =========================
    try:
        user_text = request["intent"]["slots"]["query"]["value"]
    except:
        user_text = "continue"

    memory = get_memory(session_id)

    answer = None

    # =========================
    # 🎧 SPOTIFY MODE
    # =========================
    if intent == "PlayMusicIntent":

    token = get_token(session_id)

    if not token:
        answer = "Spotify не подключен"

    else:
        access_token = token["access_token"]

        uri = search_track(user_text, access_token)

        print("TRACK URI:", uri)

        if uri:
            status = play_track(uri, access_token)

            print("PLAY STATUS:", status)

            answer = "Включаю музыку"
        else:
            answer = "Не нашёл трек"

    # =========================
    # 🤖 AI MODE (DEFAULT)
    # =========================
    else:

        answer = ask_ai(user_text, memory)
        answer = simplify_text(answer)

        # 🔥 защита от английского
        latin_ratio = sum(
            c.isascii() and c.isalpha()
            for c in answer
        ) / max(len(answer), 1)

        if latin_ratio > 0.4:
            answer = "Извини, повтори вопрос"

    # =========================
    # 💾 MEMORY SAVE
    # =========================
    save_memory(session_id, user_text, answer)

    # =========================
    # 📢 RESPONSE TO ALEXA
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

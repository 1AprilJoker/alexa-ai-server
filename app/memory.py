store = {}


def get_memory(session_id: str):
    return store.get(session_id, [])


def save_memory(session_id: str, user_text: str, assistant_text: str):

    if session_id not in store:
        store[session_id] = []

    # лёгкая защита от мусора
    if assistant_text:
        latin_ratio = sum(c.isascii() and c.isalpha() for c in assistant_text) / max(len(assistant_text), 1)

        if latin_ratio > 0.5:
            assistant_text = "Ответ сформирован некорректно"

    store[session_id].append({
        "user": user_text,
        "assistant": assistant_text
    })

    store[session_id] = store[session_id][-10:]

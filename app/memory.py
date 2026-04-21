store = {}


def get_memory(session_id: str):
    return store.get(session_id, [])


def save_memory(session_id: str, user_text: str, assistant_text: str):

    if session_id not in store:
        store[session_id] = []

    store[session_id].append({
        "user": user_text,
        "assistant": assistant_text
    })

    # ограничиваем память (важно!)
    store[session_id] = store[session_id][-10:]

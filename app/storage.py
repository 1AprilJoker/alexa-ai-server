store = {}


def save_token(user_id: str, token: dict):
    store[user_id] = token


def get_token(user_id: str):
    return store.get(user_id)

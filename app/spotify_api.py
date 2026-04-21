import requests


def get_active_device(access_token):
    r = requests.get(
        "https://api.spotify.com/v1/me/player/devices",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    devices = r.json().get("devices", [])

    if not devices:
        return None

    # берем первый активный или последний
    return devices[0]["id"]


def search_track(query, access_token):

    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "q": query,
            "type": "track",
            "limit": 3   # важно: не 1
        }
    )

    items = r.json().get("tracks", {}).get("items", [])

    if not items:
        return None

    return items[0]["uri"]


def play_track(uri, access_token):

    device_id = get_active_device(access_token)

    payload = {"uris": [uri]}

    url = "https://api.spotify.com/v1/me/player/play"

    # если есть device → добавляем его
    if device_id:
        url += f"?device_id={device_id}"

    r = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    # 🔥 ДИАГНОСТИКА
    if r.status_code >= 400:
        print("SPOTIFY ERROR:", r.text)

    return r.status_code

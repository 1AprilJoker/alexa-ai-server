import requests


def search_track(query, access_token):

    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "q": query,
            "type": "track",
            "limit": 1
        }
    )

    items = r.json()["tracks"]["items"]
    if not items:
        return None

    return items[0]["uri"]


def play_track(uri, access_token):

    requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "uris": [uri]
        }
    )

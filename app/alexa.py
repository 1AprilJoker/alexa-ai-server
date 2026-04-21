def build_response(text: str):

    ssml = f"<speak>{text}</speak>"

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": ssml
            },
            "shouldEndSession": False
        }
    }

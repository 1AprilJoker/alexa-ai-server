def build_response(text: str):

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text[:800]
            },
            "shouldEndSession": False
        }
    }

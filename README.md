# Alexa Russian AI Assistant

Voice AI backend for Amazon Alexa Skill.

## Flow
Alexa → FastAPI → OpenRouter AI → Transliteration → Alexa speech

## Deploy

### Render
1. Push repo to GitHub
2. Connect to Render
3. Add env variable:
   OPENROUTER_API_KEY
4. Deploy

## Alexa Endpoint

POST:
https://your-app.onrender.com/alexa

## Intent example

AskAIIntent:
"ask {query}"

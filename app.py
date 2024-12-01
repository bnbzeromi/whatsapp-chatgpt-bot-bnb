from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os
from langdetect import detect

app = Flask(__name__)

# Configurazioni
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """
    Gestisce i messaggi in entrata da Twilio.
    """
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()

    # Identifica la lingua del messaggio
    detected_language = detect(incoming_msg)
    if detected_language == "it":
        prompt = f"Rispondi in italiano: {incoming_msg}"
    elif detected_language == "es":
        prompt = f"Responde en español: {incoming_msg}"
    else:
        prompt = f"Reply in English: {incoming_msg}"

    # Genera una risposta con ChatGPT
    try:
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = chat_response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "C'è stato un errore nel generare la risposta. Riprova più tardi."

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)

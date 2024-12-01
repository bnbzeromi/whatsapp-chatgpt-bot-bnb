import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from langdetect import detect

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()

    try:
        detected_language = detect(incoming_msg)
        if detected_language == "it":
            prompt = f"Rispondi in italiano: {incoming_msg}"
        elif detected_language == "es":
            prompt = f"Responde en español: {incoming_msg}"
        else:
            prompt = f"Reply in English: {incoming_msg}"

        openai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        reply = openai_response["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Errore: {e}")
        reply = "C'è stato un errore nel generare la risposta. Riprova più tardi."

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    # Usa la porta fornita da Railway o una porta predefinita
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

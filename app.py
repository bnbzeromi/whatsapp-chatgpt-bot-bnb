import os
import openai
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request

app = Flask(__name__)

# Imposta la chiave API di OpenAI tramite variabile d'ambiente
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    # Ottieni il messaggio ricevuto tramite WhatsApp
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()

    try:
        print(f"Messaggio in ingresso: {incoming_msg}")  # Log del messaggio ricevuto

        # Configura il prompt in inglese
        prompt = f"Reply in English: {incoming_msg}"

        print(f"Prompt inviato a OpenAI: {prompt}")  # Log del prompt inviato a OpenAI

        # Chiamata a OpenAI
        openai_response = openai.Completion.create(
            engine="text-davinci-003",  # Modifica con il motore che preferisci
            prompt=prompt,
            max_tokens=150  # Limita il numero di token per evitare risposte troppo lunghe
        )

        # Ottieni la risposta da OpenAI
        reply = openai_response["choices"][0]["text"].strip()
        print(f"Risposta di OpenAI: {reply}")  # Log della risposta generata

    except Exception as e:
        print(f"Errore: {e}")  # Log dettagliato dell'errore
        reply = "C'è stato un errore nel generare la risposta. Riprova più tardi."

    # Invia la risposta a WhatsApp
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    # Avvia il server Flask (assicurati che Railway usi gunicorn o un altro server di produzione per il deploy)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

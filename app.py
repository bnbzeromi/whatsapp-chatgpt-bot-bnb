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

        # Chiamata a OpenAI con il modello gpt-4
        openai_response = openai.ChatCompletion.create(
            model="gpt-4",  # Usa il modello gpt-4
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150  # Limita il numero di token per evitare risposte troppo lunghe
        )

        # Ottieni la risposta da OpenAI
        reply = openai_response["choices"][0]["message"]["content"].strip()
        print(f"Risposta di OpenAI: {reply}")  # Log della risposta generata

    except openai.error.OpenAIError as e:
        print(f"Errore durante la chiamata a OpenAI: {e}")  # Log dell'errore OpenAI
        reply = "C'è stato un errore nel generare la risposta. Riprova più tardi."
    except Exception as e:
        print(f"Errore generico: {e}")  # Log di altri errori generici
        reply = "C'è stato un errore nel generare la risposta. Riprova più tardi."

    # Invia la risposta a WhatsApp
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    # Avvia il server Flask (assicurati che Railway usi gunicorn o un altro server di produzione per il deploy)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

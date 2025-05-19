from flask import Flask, request
import requests
import os
import traceback

app = Flask(__name__)

TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Tenta extrair o texto bruto do corpo
        raw_data = request.data.decode("utf-8").strip()

        # Usa isso como mensagem
        message = raw_data if raw_data else '🚨 Alerta recebido sem conteúdo.'

        send_telegram_message(message)
        return {'ok': True}, 200

    except Exception as e:
        error_trace = traceback.format_exc()
        send_telegram_message(f"❗Erro no webhook:\n<code>{error_trace}</code>")
        return {'error': str(e)}, 500

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)

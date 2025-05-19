from flask import Flask, request
import requests
import os
import traceback

app = Flask(__name__)

# === CONFIGURAÇÃO REAL ===
TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        message = data.get('message', '🚨 Alerta recebido sem mensagem específica.')

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

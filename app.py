from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === CONFIGURAÇÃO REAL ===
TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"  # ID do grupo onde as mensagens serão enviadas

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message', '🚨 Alerta recebido sem mensagem específica.')

    send_telegram_message(message)
    return {'ok': True}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # ou "Markdown" se preferir
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)

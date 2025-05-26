from flask import Flask, request
import requests
import os
import traceback

app = Flask(__name__)

TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"
GOOGLE_SHEETS_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycby0KI053Qy3VJcxfT-93X9HNvNv0s2VAyj8e3ERK8q1tkO9sHmF_Lei984XxWuJDyq8/exec"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Extrai o texto bruto do corpo da requisição
        raw_data = request.data.decode("utf-8").strip()
        message = raw_data if raw_data else '🚨 Alerta recebido sem conteúdo.'

        # Envia ao Telegram
        send_telegram_message(message)

        # Processa e envia ao Google Sheets, se o alerta contiver dados estruturados em JSON
        try:
            json_data = request.get_json(force=True)
            if json_data and isinstance(json_data, dict) and "type" in json_data:
                post_to_google_sheets(json_data)
        except Exception as parse_error:
            print("Alerta em texto livre — JSON não detectado.")

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

def post_to_google_sheets(data):
    payload = {
        "asset": data.get("asset", "XAUUSD"),
        "type": data.get("type", "Signal Alert"),
        "direction": data.get("direction", ""),
        "strength": data.get("strength", ""),
        "confidence": data.get("confidence", ""),
        "entry": data.get("entry", ""),
        "tp": data.get("tp", ""),
        "sl": data.get("sl", "")
    }
    try:
        requests.post(GOOGLE_SHEETS_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as err:
        print("Erro ao enviar para Google Sheets:", err)

if __name__ == '__main__':
    app.run(debug=True)

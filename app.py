from flask import Flask, request
import requests
import traceback

app = Flask(__name__)

TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"
GOOGLE_SHEETS_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwxHBm_4UMQnEZevT2voqCixRcD0fUP1ISdSd7vV5Q9sOrG49YP_-GU3NHFmLyg4t03/exec"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = None

        # Tenta interpretar como JSON
        try:
            json_data = request.get_json(force=True)
        except:
            pass

        # Se NÃO for JSON válido, envia como texto para o Telegram
        if not json_data or not isinstance(json_data, dict) or "type" not in json_data:
            raw_data = request.data.decode("utf-8").strip()
            message = raw_data if raw_data else '🚨 Alerta recebido sem conteúdo.'
            send_telegram_message(message)

        # Se for JSON válido, envia para Google Sheets
        if json_data and isinstance(json_data, dict) and "type" in json_data:
            post_to_google_sheets(json_data)

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
        "id": data.get("id", ""),                   # ✅ Adicionado: garante que o ID seja enviado à planilha
        "asset": data.get("asset", "XAUUSD"),
        "type": data.get("type", "Signal Alert"),
        "direction": data.get("direction", ""),
        "strength": data.get("strength", ""),
        "confidence": data.get("confidence", ""),
        "entry": data.get("entry", ""),
        "tp": data.get("tp", ""),
        "sl": data.get("sl", ""),
        "timestamp": data.get("timestamp", "")
    }
    try:
        requests.post(GOOGLE_SHEETS_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as err:
        print("Erro ao enviar para Google Sheets:", err)

if __name__ == '__main__':
    app.run(debug=True)

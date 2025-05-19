from flask import Flask, request
import requests
import os

app = Flask(__name__)

# === CONFIGURAÇÃO REAL ===
TELEGRAM_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-1002253686606"  # ID do grupo onde as mensagens serão enviadas

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Força o Flask a tratar o corpo como JSON válido
        data = request.get_json(force=True)
        message = data.get('message')

        if not message:
            message = "⚠️ Erro: Nenhuma mensagem encontrada no alerta."

        send_telegram_message(message)
        return {'ok': True}
    
    except Exception as e:
        # Em caso de falha inesperada, retorna erro
        return {'ok': False, 'error': str(e)}, 500

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

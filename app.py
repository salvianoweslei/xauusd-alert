from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7692622201:AAEDjhEdLX-mqXSgfHBimT9o6Uv9QDjyyKg"
CHAT_ID = "-4906907597"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    msg = data.get("message", "Sinal recebido")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    return {"ok": True}
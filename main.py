import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.getenv("BOT_TOKEN")
BASE_URL = f"https://bot-api.zapps.me/bot{API_KEY}"

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send response:", response.text)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Bot-Api-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Invalid secret token"}), 403

    data = request.json
    print("Webhook nhận:", data)

    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text:
            reply = f"Bạn vừa nói: {text}"
            send_message(chat_id, reply)

    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return "Zalo Bot Server đang chạy!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
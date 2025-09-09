import os
import requests

BOT_KEY = os.getenv("BOT_TOKEN")
SECRET = os.getenv("SECRET_TOKEN")

WEBHOOK_URL = "https://zalochat.onrender.com/webhook"

url = f"https://bot-api.zapps.me/bot{BOT_KEY}/setWebhook"
payload = {
    "url": WEBHOOK_URL,
    "secret_token": SECRET
}
headers = {"Content-Type": "application/json"}

res = requests.post(url, json=payload, headers=headers)
print("Status:", res.status_code)
print("Response:", res.text)

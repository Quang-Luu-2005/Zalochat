import os
import requests

BOT_KEY = os.getenv("BOT_TOKEN")
WEBHOOK_URL = "https://23e610035351.ngrok-free.app/webhook"

url = f"https://bot-api.zapps.me/bot{BOT_KEY}/setWebhook"
payload = {
    "url": WEBHOOK_URL,
    "secret_token": "my-secret-123456"
}
headers = {"Content-Type": "application/json"}

res = requests.post(url, json=payload, headers=headers)
print("Status:", res.status_code)
print("Response:", res.text)
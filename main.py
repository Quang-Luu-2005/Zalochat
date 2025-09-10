import os
from flask import Flask, request, jsonify
import requests
import random
import json
import datetime
from collections import Counter
import google.generativeai as genai
app = Flask(__name__)


GEMINI_TOKEN = os.getenv("GENIUS_API_KEY")
genai.configure(api_key=os.getenv("GENIUS_API_KEY"))
API_KEY = os.getenv("BOT_TOKEN")
BASE_URL = f"https://bot-api.zapps.me/bot{API_KEY}"

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str) -> str:
    """Gửi câu hỏi tới Gemini và trả lời"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Lỗi khi gọi Gemini: {e}"
    
def get_vietlott_today() -> str:
    """Trả về bộ số Vietlott dựa trên ngày trong tuần"""   
    today = datetime.datetime.today().weekday()

    if today in [1, 3, 5]:  # Thứ 3, 5, 7
        return f"Hôm nay là thứ {today+2}, bộ số 6/55 của bạn: {generate_vietlott_numbers(55)}"
    elif today in [2, 4, 6]:  # Thứ 4, 6, CN
        return f"Hôm nay là thứ {today+2}, bộ số 6/45 của bạn: {generate_vietlott_numbers(45)}"


def generate_vietlott_numbers(max_number: int, count: int = 6) -> str:
    """Tạo bộ số Vietlott ngẫu nhiên"""
    numbers = random.sample(range(1, max_number + 1), count)
    numbers.sort()
    return " ".join(str(n) for n in numbers)

def choose_carefully(max_number: int, simulations: int = 100, count: int = 6) -> str:
    """Chọn bộ số Vietlott dựa trên tần suất xuất hiện trong các mô phỏng"""
    freq = Counter()

    for _ in range(simulations):
        nums = random.sample(range(1, max_number + 1), count)
        freq.update(nums)

    most_common_nums = [num for num, _ in freq.most_common(count)]
    most_common_nums.sort()

    return " ".join(str(n) for n in most_common_nums)

def send_message(chat_id, text):
    """Gửi tin nhắn văn bản cho người dùng"""
    url = f"{BASE_URL}/sendMessage"
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send response:", response.text)
    return response.json()

def get_bot_reply(user_text: str) -> str:
    """
    Xử lý logic hội thoại và trả về câu trả lời
    """
    text = user_text.strip().lower()

    if text == "hello" or text == "hi" or text == "chào":
        return "Xin chào! 🤖 Mình là bot của bạn."
    elif text == "info" or text == "thông tin" or text == "giới thiệu":
        return "Mình được viết bằng Python Flask, chạy 24/7 trên Render 🚀"
    elif text == "vietlott 6/45" or text == "6/45":
        return f"Bộ số 6/45 của bạn là: {generate_vietlott_numbers(45)}"
    elif text == "vietlott 6/55" or text == "6/55":
        return f"Bộ số 6/55 của bạn là: {generate_vietlott_numbers(55)}"
    elif text == "vietlott hôm nay" or text == "cho số ngay" or text == "số ngay" or text == "số vietlott hôm nay" or text == "hôm nay":
        return get_vietlott_today()
    elif text == "vietlott careful 6/45" or text == "kỹ 6/45":
        return f"Bộ số chọn kỹ lưỡng 6/45: {choose_carefully(45)}"
    elif text == "vietlott careful 6/55" or text == "kỹ 6/55":
        return f"Bộ số chọn kỹ lưỡng 6/55: {choose_carefully(55)}"
    else:
        return ask_gemini(user_text)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Nhận sự kiện từ Zalo gửi về"""

    token = request.headers.get("X-Bot-Api-Secret-Token")
    if token != SECRET_TOKEN:
        return jsonify({"error": "Invalid secret token"}), 403

    data = request.json
    print("Webhook nhận:", data)

    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text:
            reply = get_bot_reply(text)
            send_message(chat_id, reply)

    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return "Zalo Bot Server đang chạy!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
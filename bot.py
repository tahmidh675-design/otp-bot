import requests
import time

# === Telegram Config ===
BOT_TOKEN = '7575227820:AAFhHzxKdUoFLG_0tUoc3t9fWQbKurHZuAc'
CHAT_ID = '7414697824'

# === IVAS API Config ===
IVAS_API_URL = 'https://api.sms-activate.ae/stubs/handler_api.php?'  # e.g. https://panel.com/api/messages
IVAS_API_KEY = 'YOUR_IVAS_API_KEY'  # if needed

# === (Optional) Last ID tracker ===
last_sms_id = None

def get_latest_sms():
    try:
        headers = {
            'Authorization': f'Bearer {IVAS_API_KEY}'  # Or use 'apikey': 'key' if needed
        }

        response = requests.get(IVAS_API_URL, headers=headers)

        if response.status_code == 200:
            return response.json()  # should return a list
        else:
            print("Error getting SMS:", response.text)
            return []
    except Exception as e:
        print("Exception:", e)
        return []

def send_to_telegram(msg):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'HTML'
    }
    requests.post(telegram_url, data=payload)

def format_message(sms):
    return f"""✅ <b>{sms['country']} {sms['service']} Otp Code Received Successfully.</b> 🎉

📱 <b>Number:</b> {sms['number']}
🔐 <b>OTP Code:</b> <code>{sms['otp']}</code>
🛠️ <b>Service:</b> {sms['service']}
🌍 <b>Country:</b> {sms['country']}
🕓 <b>Time:</b> {sms['timestamp']}
📝 <b>Message:</b>
<pre>{sms['message']}</pre>
"""

def main_loop():
    global last_sms_id
    print("🔄 OTP Bot is running...")

    while True:
        sms_list = get_latest_sms()

        for sms in sms_list:
            sms_id = sms.get("id")
            if sms_id != last_sms_id:
                message = format_message(sms)
                send_to_telegram(message)
                last_sms_id = sms_id
                print("✅ New OTP sent to Telegram.")
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main_loop()

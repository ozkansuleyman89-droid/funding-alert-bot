import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    r = requests.post(url, data=payload)

    print("Telegram Status:", r.status_code)
    print(r.text)


def main():
    print("Funding Alarm Bot Başladı")

    send_telegram(
        "🚀 Funding Alarm Bot başarıyla başlatıldı.\n\n"
        "Şu an test modunda çalışıyor."
    )

    while True:
        print("Bot çalışıyor...")
        time.sleep(60)


if __name__ == "__main__":
    main()

import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BINANCE_URL = "https://fapi.binance.com/fapi/v1/premiumIndex"

# Sadece -0.10% ve daha düşük fundingleri göster
FUNDING_LIMIT = -0.001

last_message = ""


def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=10
    )


def get_funding():
    r = requests.get(BINANCE_URL, timeout=15)
    r.raise_for_status()
    return r.json()


print("Funding Bot Başladı")
telegram("✅ Funding Bot yeniden başlatıldı.")

while True:

    try:

        funding = get_funding()

        negatives = []

        for coin in funding:

            rate = float(coin["lastFundingRate"])

            if rate <= FUNDING_LIMIT:
                negatives.append((coin["symbol"], rate))

        negatives.sort(key=lambda x: x[1])

        if len(negatives) == 0:
            text = "📉 Şu anda filtreye uyan negatif funding bulunamadı."
        else:
            text = "📉 Negatif Funding Alarmı\n\n"

            for symbol, rate in negatives[:10]:
                text += f"{symbol}\n{rate*100:.4f}%\n\n"

        if text != last_message:
            telegram(text)
            last_message = text
            print("Telegram gönderildi.")
        else:
            print("Değişiklik yok.")

    except Exception as e:
        print(e)
        telegram(f"❌ Hata:\n{e}")

    time.sleep(300)

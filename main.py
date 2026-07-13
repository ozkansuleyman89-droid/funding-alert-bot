import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BINANCE_URL = "https://fapi.binance.com/fapi/v1/premiumIndex"


def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


def get_funding():

    r = requests.get(BINANCE_URL, timeout=10)

    data = r.json()

    return data


print("Funding Bot Başladı")

telegram("✅ Binance Funding Bot başladı.")

while True:

    try:

        funding = get_funding()

        negatives = []

        for coin in funding:

            rate = float(coin["lastFundingRate"])

            if rate < 0:

                negatives.append((coin["symbol"], rate))

        negatives.sort(key=lambda x: x[1])

        text = "📉 En Negatif İlk 10 Funding\n\n"

        for symbol, rate in negatives[:10]:

            text += f"{symbol}  {rate*100:.4f}%\n"

        telegram(text)

    except Exception as e:

        telegram(str(e))

    time.sleep(300)

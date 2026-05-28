import time
import requests
import yfinance as yf

# 🔴 ضع بياناتك هنا
BOT_TOKEN="8757386123:AAEtru7iStzR8-61gfbiF8WUC8qEfc9b-j0"
CHAT_ID = "1592996061"


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Send error:", e)


def get_price():
    data = yf.Ticker("XAUUSD=X").history(period="5d", interval="15m")
    return data["Close"]


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


def signal(value):
    if value < 30:
        return "🟢 BUY"
    elif value > 70:
        return "🔴 SELL"
    else:
        return "⚪ WAIT"


send("🚀 Bot Started (Test Version)")

while True:
    try:
        prices = get_price()
        value = rsi(prices).iloc[-1]

        msg = f"""
📊 GOLD XAUUSD

RSI: {round(value, 2)}
Signal: {signal(value)}
"""

        send(msg)

    except Exception as e:
        send(f"Error: {str(e)}")

    time.sleep(300)
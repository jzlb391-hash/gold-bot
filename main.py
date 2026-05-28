import requests
import time
import yfinance as yf

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "1592996061"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_price():
    data = yf.Ticker("XAUUSD=X").history(period="5d", interval="15m")
    return data["Close"]

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def signal(rsi_value):
    if rsi_value < 30:
        return "🟢 شراء"
    elif rsi_value > 70:
        return "🔴 بيع"
    else:
        return "⚪ لا صفقة"

send("🚀 Bot Started")

while True:
    try:
        prices = get_price()
        value = rsi(prices).iloc[-1]

        msg = f"""
📊 XAUUSD LIVE

RSI: {round(value,2)}
Signal: {signal(value)}
"""
        send(msg)

    except Exception as e:
        send(str(e))

    time.sleep(300)

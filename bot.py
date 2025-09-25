import os
import time
import requests
import telebot
from threading import Thread

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
INTERVAL = int(os.getenv("POLL_INTERVAL", 3600))

bot = telebot.TeleBot(TOKEN)

# --- Получение курсов валют ---
def get_exchange_rates():
    # Здесь имитация данных (можно подключить API банка)
    return {
        "USD": 12600,
        "EUR": 13400,
        "RUB": 130,
        "KZT": 27,
        "CNY": 1720
    }

# --- Получение криптовалют ---
def get_crypto_rates():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,toncoin,tether", "vs_currencies": "usd"}
    r = requests.get(url, params=params).json()
    return {
        "BTC": r["bitcoin"]["usd"],
        "ETH": r["ethereum"]["usd"],
        "TON": r["toncoin"]["usd"],
        "USDT": r["tether"]["usd"]
    }

# --- Формирование текста ---
def format_message():
    rates = get_exchange_rates()
    crypto = get_crypto_rates()

    text = "💱 Курсы валют (обновление раз в час):\n\n"
    text += f"🇺🇸 USD: {rates['USD']} сум\n"
    text += f"🇪🇺 EUR: {rates['EUR']} сум\n"
    text += f"🇷🇺 RUB: {rates['RUB']} сум\n"
    text += f"🇰🇿 KZT: {rates['KZT']} сум\n"
    text += f"🇨🇳 CNY: {rates['CNY']} сум\n\n"

    text += "🪙 Криптовалюты:\n"
    text += f"₿ Bitcoin: {crypto['BTC']}$\n"
    text += f"Ξ Ethereum: {crypto['ETH']}$\n"
    text += f"TON: {crypto['TON']}$\n"
    text += f"Tether (USDT): {crypto['USDT']}$\n"

    return text

# --- Цикл обновления ---
def updater():
    while True:
        try:
            msg = format_message()
            bot.send_message(CHANNEL_ID, msg)
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(INTERVAL)

# --- Запуск ---
def run():
    Thread(target=updater, daemon=True).start()
    bot.infinity_polling()

if __name__ == "__main__":
    run()

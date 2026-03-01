import telebot
import requests

TOKEN = "8520147468:AAFR940FT2D9O2xWfgQZd5dB5fRZ0YAD9PY"
bot = telebot.TeleBot(TOKEN)

# Стартовая команда теперь просто ничего не отвечает
@bot.message_handler(commands=['start'])
def start(message):
    # Можно просто ничего не делать
    pass

@bot.message_handler(func=lambda message: True)
def download(message):
    if "tiktok.com" in message.text:
        url = "https://tikwm.com/api/?url=" + message.text
        try:
            r = requests.get(url).json()
            video = r["data"]["play"]
            bot.send_video(message.chat.id, video)
        except Exception as e:
            bot.send_message(message.chat.id, "Не удалось скачать видео.")
    else:
        # Если это не ссылка на TikTok, можно не отвечать или написать что-то вроде:
        pass

bot.remove_webhook()
bot.polling()
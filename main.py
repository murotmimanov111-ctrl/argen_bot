import telebot
from telebot import types
import feedparser
import schedule
import time
import threading
import requests

# Токен
TOKEN = '8819884297:AAHy8KoZA7pgLLflecQkQn64KhDlKmb9sTc'
bot = telebot.TeleBot(TOKEN)

# Булактар
NEWS_FEEDS = ["https://akipress.org/rss/akipress.rss", "https://24.kg/rss/"]
sent_articles = set()

def get_latest_news(limit=3):
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for feed_url in NEWS_FEEDS:
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                articles.extend(feed.entries[:limit])
        except Exception: continue
    return articles

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Акыркы жаңылыктар"), types.KeyboardButton("📢 Жарнама / Байланыш"))
    bot.send_message(message.chat.id, "👋 Салам! Жаңылыктар ботуна кош келиңиз.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📰 Акыркы жаңылыктар")
def send_news(message):
    entries = get_latest_news(limit=3)
    if not entries:
        bot.send_message(message.chat.id, "❌ Жаңылыктар учурда жеткиликсиз.")
        return
    for entry in entries:
        text = f"📰 **{entry.title}**\n\n🔗 [Толук окуу]({entry.link})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "📢 Жарнама / Байланыш")
def ads_info(message):
    # Сиз каалаган маалымат
    text = "📢 **Жарнама берүү үчүн байланыш:**\n\n📞 +996 999906700\n💳 simbank"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# Ботту ишке киргизүү
if __name__ == "__main__":
    # Эски туташууларды тазалоо (409 катасын болтурбоо үчүн)
    try:
        bot.remove_webhook()
        print("Бот ишке кирди...")
        # infinity_polling ката болсо өзү кайра аракет кылат
        bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Ката: {e}")

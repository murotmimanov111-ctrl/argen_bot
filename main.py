import telebot
from telebot import types
import feedparser
import schedule
import time
import threading
import re

TOKEN = '8819884297:AAHy8KoZA7pgLLflecQkQn64KhDlKmb9sTc'
bot = telebot.TeleBot(TOKEN)

# Кыргызстандагы бир нече туруктуу жаңылыктар булагы
NEWS_FEEDS = [
    "https://akipress.org/rss/akipress.rss",
    "https://24.kg/rss/",
    "https://kabar.kg/kg/news/rss/"
]

sent_articles = set()

def extract_image_url(entry):
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    if 'links' in entry:
        for link in entry.links:
            if link.get('type', '').startswith('image/'):
                return link['href']
    description = entry.get('description', '')
    img_match = re.search(r'src=["\'](https?://[^"\']+\.(?:jpg|png|jpeg))["\']', description)
    if img_match:
        return img_match.group(1)
    return None

def get_latest_news(limit=3):
    articles = []
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            if feed.entries:
                for entry in feed.entries[:limit]:
                    articles.append(entry)
                if articles:
                    break
        except Exception as e:
            continue
    return articles

def auto_send_news():
    try:
        entries = get_latest_news(limit=1)
        if not entries:
            return

        latest = entries[0]
        article_id = latest.get('id', latest.link)

        if article_id not in sent_articles:
            sent_articles.add(article_id)
            print(f"Жаңы жаңылык табылды: {latest.title}")
    except Exception as e:
        print(f"Ката: {e}")

def scheduler_thread():
    schedule.every(10).minutes.do(auto_send_news)
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 Акыркы жаңылыктар")
    btn2 = types.KeyboardButton("📢 Жарнама / Байланыш")
    markup.add(btn1, btn2)
    bot.reply_to(message, "👋 Салам! Кыргызстандагы акыркы жаңылыктарды ушул боттон көрө аласыз.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📰 Акыркы жаңылыктар")
def send_manual_news(message):
    msg = bot.reply_to(message, "⏳ Жаңылыктар жүктөлүүдө...")
    
    entries = get_latest_news(limit=3)
    
    if not entries:
        bot.edit_message_text("❌ Жаңылыктар табылган жок. Кайра аракет кылып көрүңүз.", message.chat.id, msg.message_id)
        return

    bot.delete_message(message.chat.id, msg.message_id)

    for entry in entries:
        title = entry.title
        link = entry.link
        img_url = extract_image_url(entry)
        text = f"📰 **{title}**\n\n🔗 [Толук окуу]({link})"

        if img_url:
            try:
                bot.send_photo(message.chat.id, img_url, caption=text, parse_mode="Markdown")
            except:
                bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=False)
        else:
            bot.send_message(message.chat.id, text, parse_mode="Markdown", disable_web_page_preview=False)

@bot.message_handler(func=lambda message: message.text == "📢 Жарнама / Байланыш")
def ads_info(message):
    bot.reply_to(message, "📢 **Жарнама берүү үчүн:**\n\nАдминге жазыңыз: @админ_логин", parse_mode="Markdown")

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)

    t = threading.Thread(target=scheduler_thread)
    t.daemon = True
    t.start()

    bot.infinity_polling(skip_pending=True)

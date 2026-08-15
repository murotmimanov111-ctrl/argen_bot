import telebot
from telebot import types
import feedparser
import requests

# Токен
TOKEN = '8819884297:AAEZKOJOzQv9BAVEpz36bDxhYZHbcV_Hpsc'
bot = telebot.TeleBot(TOKEN)

NEWS_FEEDS = [
    "https://akipress.org/rss/akipress.rss",
    "https://24.kg/rss/"
]

def get_latest_news(query=None, limit=3):
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for feed_url in NEWS_FEEDS:
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    if query:
                        if query.lower() in entry.title.lower() or query.lower() in entry.summary.lower():
                            articles.append(entry)
                    else:
                        articles.append(entry)
                    if len(articles) >= limit:
                        break
        except Exception:
            continue
        if len(articles) >= limit:
            break
    return articles

# Жарнама тексти
ADS_TEXT = (
    "📝 **ЖАРНАМАГА ӨТҮНМӨ (ЗАЯВКА) БЕРҮҮ**\n\n"
    "💰 **Жарнама баасы:** 100 сом\n"
    "🏦 **Банктын аты:** simbank\n"
    "📞 **Байланыш/Төлөм номери:** +996 999906700\n\n"
    "⚠️ **Шарттары:** Төлөмдү **simbank** аркылуу аткаргандан кийин, чекти (скриншотту) ушул ботко жөнөтүңүз."
)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📰 Акыркы жаңылыктар"))
    markup.add(types.KeyboardButton("📢 Жарнама / Байланыш"), types.KeyboardButton("📝 Жарнамага өтүнмө берүү"))
    
    text = (
        "👋 Салам! Кыргызстан жаңылыктары ботуна кош келиңиз.\n\n"
        "📰 **Жаңылык издөө:** каалаган сөздү жазыңыз (мисалы: `доллар`).\n"
        "▶️ **Видео издөө:** 'video' сөзү менен баштаңыз (мисалы: `video футбол`)."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📰 Акыркы жаңылыктар")
def send_news(message):
    entries = get_latest_news(limit=3)
    for entry in entries:
        text = f"📰 **{entry.title}**\n\n🔗 [Толук окуу]({entry.link})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text in ["📢 Жарнама / Байланыш", "📝 Жарнамага өтүнмө берүү"])
def ads_info(message):
    bot.send_message(message.chat.id, ADS_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_user_text(message):
    user_text = message.text.strip()
    
    # 1. Видео издөө (эгер 'video' менен баштаса)
    if user_text.lower().startswith("video"):
        search_query = user_text.replace("video", "").strip()
        if not search_query:
            bot.reply_to(message, "⚠️ Сураныч, видеонун атын жазыңыз. Мисалы: `video футбол`", parse_mode="Markdown")
        else:
            url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            bot.reply_to(message, f"▶️ **'{search_query}'** боюнча табылган видеолор:\n\n🔗 [YouTube'дан көрүү]({url})", parse_mode="Markdown")
        return

    # 2. Шилтеме/Чек текшерүү
    if "http://" in user_text or "https://" in user_text or "t.me" in user_text:
        bot.reply_to(message, "❌ **Кечиресиз, жарнама баасы 100 сом.**\nЖарнама шилтемесин жайгаштыруу үчүн **simbank** аркылуу 100 сом төлөп, чекти жөнөтүңүз.", parse_mode="Markdown")
        return

    # 3. Жаңылык издөө
    msg = bot.reply_to(message, f"🔍 **'{user_text}'** боюнча жаңылыктар изделүүдө...")
    entries = get_latest_news(query=user_text, limit=3)
    
    if not entries:
        bot.edit_message_text(f"❌ **'{user_text}'** боюнча жаңылык табылган жок.", message.chat.id, msg.message_id, parse_mode="Markdown")
        return

    bot.delete_message(message.chat.id, msg.message_id)
    for entry in entries:
        text = f"📰 **{entry.title}**\n\n🔗 [Толук окуу]({entry.link})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)

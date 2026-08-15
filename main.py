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

# Жарнама жана өтүнмө тексти
ADS_TEXT = (
    "📝 **ЖАРНАМАГА ӨТҮНМӨ (ЗАЯВКА) БЕРҮҮ**\n\n"
    "💰 **Жарнама баасы:** 100 сом\n"
    "🏦 **Банктын аты:** simbank\n"
    "📞 **Байланыш/Төлөм номери:** +996 999906700\n\n"
    "⚠️ **Шарттары:** Төлөмдү **simbank** аркылуу аткаргандан кийин, чекти (скриншотту же шилтемени) ушул ботко жөнөтүңүз."
)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 Акыркы жаңылыктар")
    btn2 = types.KeyboardButton("📢 Жарнама / Байланыш")
    btn3 = types.KeyboardButton("📝 Жарнамага өтүнмө берүү")
    
    # Кнопкаларды жайгаштыруу
    markup.add(btn1)
    markup.add(btn2, btn3)
    
    text = (
        "👋 Салам! Кыргызстан жаңылыктары ботуна кош келиңиз.\n\n"
        "🔍 **Каалаган жаңылыгыңызды табуу үчүн** темасын же сөз жазып жөнөтүңүз.\n"
        "Мисалы: `доллар`, `Бишкек`, `спорт`"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📰 Акыркы жаңылыктар")
def send_news(message):
    entries = get_latest_news(limit=3)
    if not entries:
        bot.send_message(message.chat.id, "❌ Жаңылыктар учурда жеткиликсиз.")
        return
    for entry in entries:
        text = f"📰 **{entry.title}**\n\n🔗 [Толук окуу]({entry.link})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

# "Жарнама / Байланыш" же "Жарнамага өтүнмө берүү" баскычы басылганда
@bot.message_handler(func=lambda message: message.text in ["📢 Жарнама / Байланыш", "📝 Жарнамага өтүнмө берүү"])
def ads_info(message):
    bot.send_message(message.chat.id, ADS_TEXT, parse_mode="Markdown")

# Чек же шилтеме (фото/документ түрүндө) келгенде
@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    bot.reply_to(
        message, 
        "❌ **Кечиресиз, жарнама баасы 100 сомду түзөт.**\n"
        "Сиз жөнөткөн төлөм тастыктамасы текшерилди: сумма 100 сомдон аз же туура эмес. Сураныч, **simbank** аркылуу толук 100 сом которуп, чекти кайра жөнөтүңүз.", 
        parse_mode="Markdown"
    )

# Текст түрүндө суроо же шилтеме жазганда
@bot.message_handler(func=lambda message: True)
def handle_user_text(message):
    user_text = message.text.strip()
    
    # Шилтеме жөнөтүлсө
    if "http://" in user_text or "https://" in user_text or "t.me" in user_text:
        bot.reply_to(
            message, 
            "❌ **Кечиресиз, жарнама баасы 100 сомду түзөт.**\n"
            "Жарнама шилтемесин жайгаштыруу үчүн **simbank** аркылуу 100 сом төлөп, чегин жөнөтүңүз.", 
            parse_mode="Markdown"
        )
        return

    # Жаңылык издөө
    msg = bot.reply_to(message, f"🔍 **'{user_text}'** боюнча жаңылыктар изделүүдө...")
    entries = get_latest_news(query=user_text, limit=3)
    
    if not entries:
        bot.edit_message_text(f"❌ **'{user_text}'** боюнча эч кандай жаңылык табылган жок. Башка сөз менен издеп көрүңүз.", message.chat.id, msg.message_id, parse_mode="Markdown")
        return

    bot.delete_message(message.chat.id, msg.message_id)
    for entry in entries:
        text = f"📰 **{entry.title}**\n\n🔗 [Толук окуу]({entry.link})"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Ката: {e}")

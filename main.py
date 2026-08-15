import telebot
from telebot import types
import feedparser
import schedule
import time
import threading
import re

# Токен
TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

# Кыргызстандын жаңылыктар булагы (RSS)
NEWS_FEED = "https://kabar.kg/kg/news/rss/"

# Мурда жөнөтүлгөн жаңылыктарды эстеп калуу үчүн
sent_articles = set()

# Сүрөттү RSS ичинен таап алуу функциясы
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

# Автоматтык түрдө жаңылыктарды текшерүү
def auto_send_news():
    try:
        feed = feedparser.parse(NEWS_FEED)
        if not feed.entries:
            return

        latest = feed.entries[0]
        article_id = latest.get('id', latest.link)

        if article_id not in sent_articles:
            sent_articles.add(article_id)
            title = latest.title
            link = latest.link
            image_url = extract_image_url(latest)

            caption = f"📰 **СОҢКУ ЖАҢЫЛЫК**\n\n**{title}**\n\n🔗 [Толук окуу]({link})"

            # Бул жерге өзүңүздүн каналдын атын же чат ID жазсаңыз болот (мисалы: "@my_channel")
            # Азырынча консолго маалымат чыгарат
            print(f"Жаңы жаңылык табылды: {title}")
    except Exception as e:
        print(f"Жаңылык алууда ката: {e}")

# Таймер
def scheduler_thread():
    # Ар 10 мүнөттө жаңылыктарды текшерет
    schedule.every(10).minutes.do(auto_send_news)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Боттун кнопкалары жана командалары
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📰 Акыркы жаңылыктар")
    btn2 = types.KeyboardButton("📢 Жарнама / Байланыш")
    markup.add(btn1, btn2)
    bot.reply_to(message, "👋 Салам! Кыргызстан жаңылыктарын жана жарнамаларды ушул боттон көрө аласыз.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📰 Акыркы жаңылыктар")
def send_manual_news(message):
    msg = bot.reply_to(message, "⏳ Жаңылыктар загрузка болуп жатат...")
    try:
        feed = feedparser.parse(NEWS_FEED)
        if not feed.entries:
            bot.edit_message_text("❌ Жаңылыктар табылган жок.", message.chat.id, msg.message_id)
            return

        for entry in feed.entries[:3]:
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
        
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ Ката кетти, кайра аракет кылыңыз.", message.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: message.text == "📢 Жарнама / Байланыш")
def ads_info(message):
    bot.reply_to(message, "📢 **Жарнама берүү үчүн:**\n\nАдминге жазыңыз: @админ_логин", parse_mode="Markdown")

if __name__ == "__main__":
    # 409 катасын алдын алуу үчүн эски байланыштарды тазалоо
    bot.remove_webhook()
    time.sleep(2)

    # Таймерди өзүнчө агымда баштоо
    t = threading.Thread(target=scheduler_thread)
    t.daemon = True
    t.start()

    print("Бот иштеп баштады...")
    # skip_pending=True эски сурамдарды тазалап, катаны болтурбайт
    bot.infinity_polling(skip_pending=True)

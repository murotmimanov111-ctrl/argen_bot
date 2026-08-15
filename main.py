import telebot
import feedparser
import schedule
import time
import threading
import re

TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

# Кыргызстандын жаңылыктар булагы
NEWS_FEED = "https://kabar.kg/kg/news/rss/"

# Соңку жөнөтүлгөн жаңылыктардын ID же шилтемелери (кайталанбашы үчүн)
sent_articles = set()

# Сүрөттү RSS ичинен бөлүп алуу функциясы
def extract_image_url(entry):
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0]['url']
    if 'links' in entry:
        for link in entry.links:
            if link.get('type', '').startswith('image/'):
                return link['href']
    # Эгер сүрөт сыпаттамада (description) катылса
    description = entry.get('description', '')
    img_match = re.search(r'src=["\'](https?://[^"\']+\.(?:jpg|png|jpeg))["\']', description)
    if img_match:
        return img_match.group(1)
    return None

# Автоматтык түрдө жаңылык жөнөтүүчү функция
def auto_send_news():
    try:
        feed = feedparser.parse(NEWS_FEED)
        if not feed.entries:
            return

        # Эң акыркы жаңылыкты алуу
        latest = feed.entries[0]
        article_id = latest.get('id', latest.link)

        # Эгер бул жаңылык мурда жөнөтүлбөгөн болсо
        if article_id not in sent_articles:
            sent_articles.add(article_id)
            
            title = latest.title
            link = latest.link
            image_url = extract_image_url(latest)

            caption_text = f"📰 **ЖАҢЫ КУЛАКТАНДУУ / ЖАҢЫЛЫК**\n\n**{title}**\n\n🔗 [Толук окуу]({link})"

            # Төмөнкү жерге өзүңүздүн Телеграм каналыңыздын ID'син же колдонуучунун chat_id кошуңуз
            # Мисалы: CHAT_ID = "@сиздин_каналдын_аты" же чат ID
            # Азырынча тест катары ботту иштеткен чатка кетет
            
            # Эгер сүрөтү бар болсо сүрөтү менен, жок болсо текст түрүндө жөнөтөт
            # (Эскертүү: Каналга же чатка жөнөтүү үчүн CHAT_ID жазылат)
            print(f"Жаңы жаңылык табылды: {title}")

    except Exception as e:
        print(f"Ката кетти: {e}")

# Таймерди өзүнчө агымда (thread) иштетүү
def scheduler_thread():
    # Интервалды өзгөртсөңүз болот: 10 мүнөт, 30 мүнөт же 1 саат
    schedule.every(10).minutes.do(auto_send_news)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Салам! Бот иштеп жатат. Жаңы жаңылыктар автоматтык түрдө келип турат.")

if __name__ == "__main__":
    bot.remove_webhook()
    
    # Таймерди фондо иштетүү
    t = threading.Thread(target=scheduler_thread)
    t.daemon = True
    t.start()
    
    print("Бот жана таймер ишке түштү...")
    bot.infinity_polling()

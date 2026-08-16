import telebot
from urllib.parse import quote

# Сенин бот токениң
TOKEN = '8961768379:AAGVtgfAjWmJx_j7zVBGzhEipecDPZnXY5w'
bot = telebot.TeleBot(TOKEN)

# /start командасы үчүн жылуу учурашуу
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Салам, досум! 🌟🎶\n\n"
        "Музыка – бул жашоонун көркү! Мага каалаган ырыңдын атын же ырчыны жазсаң, "
        "мен сага эң сонун шилтемелерди заматта таап берем! 🔥💃\n\n"
        "Кандай ыр угабыз? Жаза гой! 🎧✨"
    )
    bot.reply_to(message, welcome_text)

# Ырды издеп, эмоция менен жооп берүү
@bot.message_handler(func=lambda message: True)
def search_song(message):
    query = message.text
    encoded_query = quote(query)  # Текстти URL форматына айлантуу
    
    # Издөө шилтемелери
    google_url = f"https://www.google.com/search?q={encoded_query}+ыр+скачать"
    youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    # Супер позитивдүү жана эмоциялуу текст
    text = (
        f"Ооба-а-а! Эң сонун тандоо! 🥳🎶\n\n"
        f"Ушул <b>«{query}»</b> деген сонун ырды сен үчүн издеп таптым! 💥👇\n\n"
        f"🔍 <a href='{google_url}'>Google'дон ырды табуу жана жүктөө 📥</a>\n"
        f"🎬 <a href='{youtube_url}'>YouTube'дон клибин көрүү жана угуу 🎧</a>\n\n"
        f"Музыка маанайыңды көтөрсүн! Каалаган убакта кайра жаза бер! 🥰✨"
    )
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)

# Ботту үзгүлтүксүз иштетүү
bot.polling(none_stop=True)

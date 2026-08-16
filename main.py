import telebot
from urllib.parse import quote

# Телеграм боттун токенин ушу жерге жазыңыз
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салам! Мага каалаган ырдын атын же аткаруучусун жазыңыз, мен сизге Google жана YouTube'дан табуу шилтемесин түзүп берем.")

@bot.message_handler(func=lambda message: True)
def search_song(message):
    query = message.text
    encoded_query = quote(query)  # Текстти URL форматына айлантуу
    
    # Издөө шилтемелерин түзүү
    google_url = f"https://www.google.com/search?q={encoded_query}+ыр+скачать"
    youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
    
    text = (
        f"🎵 <b>«{query}»</b> ырын издөө шилтемелери:\n\n"
        f"🔍 <a href='{google_url}'>Google'дон издөө</a>\n"
        f"🎬 <a href='{youtube_url}'>YouTube'дон көрүү</a>"
    )
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)

bot.polling(none_stop=True)

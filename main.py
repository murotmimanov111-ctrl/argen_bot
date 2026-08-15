import telebot
from telebot import types
from youtubesearchpython import VideosSearch

TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌍 Салам! Ыр издөө үчүн: **+ ырдын аты** деп жаз.")

@bot.message_handler(func=lambda message: message.text.startswith('+'))
def find_song(message):
    query = message.text[1:].strip()
    if not query:
        return

    bot.reply_to(message, "⏳ Ырлар изделүүдө...")

    try:
        videosSearch = VideosSearch(query, limit=5)
        results = videosSearch.result()['result']
        
        if not results:
            bot.reply_to(message, "❌ Ыр табылган жок.")
            return

        # Натыйжаларды калыптандыруу
        response_text = "🎵 Табылган ырлар:\n\n"
        markup = types.InlineKeyboardMarkup()

        for i, video in enumerate(results, 1):
            title = video['title']
            duration = video.get('duration', 'N/A')
            link = video['link']
            
            # Текстке кошуу
            response_text += f"{i}. {title} ({duration})\n"
            
            # Баскычтарды кошуу
            button = types.InlineKeyboardButton(f"{i}", url=link)
            markup.add(button)

        bot.reply_to(message, response_text, reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ката кетти: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()

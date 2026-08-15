import telebot
from youtube_search import YoutubeSearch

# Сиздин токениңиз
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

    bot.reply_to(message, "⏳ Ыр изделип жатат...")

    try:
        # Издеп көрүү
        results = YoutubeSearch(query, max_results=1).to_dict()
        
        if results:
            song = results[0]
            title = song['title']
            url = f"https://www.youtube.com{song['url_suffix']}"
            bot.reply_to(message, f"✅ Таптым:\n🎵 {title}\n🔗 {url}")
        else:
            bot.reply_to(message, "❌ Ыр табылган жок.")
    except Exception as e:
        bot.reply_to(message, "⚠️ Ката кетти, кийинчерээк аракет кыл.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()

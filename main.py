import telebot
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

    bot.reply_to(message, "⏳ Ыр изделип жатат...")

    try:
        # Туура импорттолгон VideosSearch колдонобуз
        videosSearch = VideosSearch(query, limit=1)
        results = videosSearch.result()
        
        if results and 'result' in results and len(results['result']) > 0:
            song = results['result'][0]
            title = song['title']
            url = song['link']
            bot.reply_to(message, f"✅ Таптым:\n🎵 {title}\n🔗 {url}")
        else:
            bot.reply_to(message, "❌ Ыр табылган жок.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ката кетти: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()

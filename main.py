import telebot
from telebot import types
from yt_dlp import YoutubeDL

TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌍 Салам! Ыр издөө үчүн: **+ ырдын аты** деп жаз.\nМисалы: `+ белом самолете`")

@bot.message_handler(func=lambda message: message.text.startswith('+'))
def find_song(message):
    query = message.text[1:].strip()
    if not query:
        return

    bot.reply_to(message, "⏳ Ыр изделүүдө...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch5', # 5 ыр издейт
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            results = info.get('entries', [])

            if not results:
                bot.reply_to(message, "❌ Ыр табылган жок.")
                return

            response_text = "🎵 **Табылган ырлар:**\n\n"
            markup = types.InlineKeyboardMarkup()

            for i, video in enumerate(results, 1):
                title = video.get('title', 'Белгисиз')
                url = video.get('webpage_url', '')
                
                response_text += f"{i}. {title}\n"
                button = types.InlineKeyboardButton(f"▶️ {i}-ырды угуу", url=url)
                markup.add(button)

            bot.reply_to(message, response_text, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, "⚠️ Издөөдө ката чыкты. Кайра аракет кылып көрүңүз.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()

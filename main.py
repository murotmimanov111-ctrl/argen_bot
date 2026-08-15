import telebot

# Сиздин токениңиз
TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

# Ырлардын базасы
songs = {
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "believer": "https://www.youtube.com/watch?v=7PCkvCPvDXk",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Салам! Мен музыкалык ботмун.\nЫр издеш үчүн: **+ ырдын аты** деп жаз.\nМисалы: `+ despacito`")

@bot.message_handler(func=lambda message: message.text.startswith('+'))
def find_song(message):
    query = message.text[1:].strip().lower()
    if query in songs:
        bot.reply_to(message, f"✅ Таптым: {query.upper()}\nШилтеме: {songs[query]}")
    else:
        bot.reply_to(message, "❌ Кечиресиз, бул ыр базада жок экен.")

if __name__ == "__main__":
    print("Бот иштеп жатат...")
    # 409 катасын алдын алуу үчүн web-hookту тазалайбыз
    bot.remove_webhook()
    # Эски параметрлерди алып салдык, эми ката бербейт
    bot.infinity_polling()

import telebot

TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

# Ырлардын базасы (Бул жерге каалаганча ыр кошо берсең болот)
songs = {
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "believer": "https://www.youtube.com/watch?v=7PCkvCPvDXk",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
    "salam": "https://www.youtube.com/watch?v=example_link"
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Салам! Мен музыкалык ботмун.\nЫр издеш үчүн: **+ ырдын аты** деп жаз.\nМисалы: `+ despacito`")

@bot.message_handler(func=lambda message: message.text.startswith('+'))
def find_song(message):
    # '+' белгисин алып салып, атын тазалайбыз
    query = message.text[1:].strip().lower()
    
    # Эгер базада бар болсо
    if query in songs:
        bot.reply_to(message, f"✅ Таптым: {query.upper()}\nШилтеме: {songs[query]}")
    else:
        bot.reply_to(message, "❌ Кечиресиз, бул ыр базада жок экен. Атын туура жаздыңызбы?")

# drop_pending_updates=True бул жерде да сөзсүз керек, ката бербеш үчүн
print("Музыкалык бот иштеп жатат...")
bot.infinity_polling(drop_pending_updates=True)

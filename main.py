import telebot
from telebot import types
import urllib.parse

# Жаңы токениңиз
TOKEN = '8819884297:AAEZKOJOzQv9BAVEpz36bDxhYZHbcV_Hpsc'
bot = telebot.TeleBot(TOKEN)

# Жарнама тексти жана реквизиттер
ADS_TEXT = (
    "📝 **ЖАРНАМАГА ӨТҮНМӨ (ЗАЯВКА) БЕРҮҮ**\n\n"
    "💰 **Жарнама баасы:** 100 сом\n"
    "🏦 **Банктын аты:** simbank\n"
    "📞 **Байланыш/Төлөм номери:** +996 999906700\n\n"
    "⚠️ **Шарттары:** Төлөмдү **simbank** аркылуу аткаргандан кийин, чекти (скриншотту) ушул ботко жөнөтүңүз."
)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎬 Видео издөө")
    btn2 = types.KeyboardButton("🎵 Музыка издөө")
    btn3 = types.KeyboardButton("📝 Жарнамага өтүнмө берүү")
    
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    text = (
        "👋 **Салам! Видео жана Музыка издөөчү ботко кош келиңиз.**\n\n"
        "🔍 **Кантип издөө керек?**\n"
        "• Каалаган ырдын же видеонун атын жөн гана жазыңыз (мисалы: `Bakr - Венера` же `BMW M5 F90`).\n"
        "• Мүмкүнчүлүктөрдү көрүү үчүн төмөнкү баскычтарды колдонуңуз."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["📢 Жарнама / Байланыш", "📝 Жарнамага өтүнмө берүү"])
def ads_info(message):
    bot.send_message(message.chat.id, ADS_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🎬 Видео издөө")
def video_help(message):
    bot.send_message(message.chat.id, "🎬 **Көрүүнү каалаган видеонун атын жазып жөнөтүңүз.**\nМисалы: `футбол тренд` же `клиптер`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🎵 Музыка издөө")
def music_help(message):
    bot.send_message(message.chat.id, "🎵 **Угууну каалаган музыканын же ырчынын атын жазып жөнөтүңүз.**\nМисалы: `Bakr` же `казакша ырлар`", parse_mode="Markdown")

# Чек же сүрөт келгенде
@bot.message_handler(content_types=['photo', 'document'])
def handle_receipt(message):
    bot.reply_to(
        message, 
        "❌ **Кечиресиз, жарнама баасы 100 сомду түзөт.**\n"
        "Сиз жөнөткөн төлөм тастыктамасы текшерилди: сумма 100 сомдон аз же туура эмес. Сураныч, **simbank** аркылуу толук 100 сом которуп, чекти кайра жөнөтүңүз.", 
        parse_mode="Markdown"
    )

# Колдонуучы текст жазганда издөө
@bot.message_handler(func=lambda message: True)
def search_media(message):
    user_text = message.text.strip()
    
    # Эгер шилтеме (ссылка) жөнөтсө — жарнама эскертүүсү чыгат
    if "http://" in user_text or "https://" in user_text or "t.me" in user_text:
        bot.reply_to(
            message, 
            "❌ **Кечиресиз, жарнама баасы 100 сомду түзөт.**\n"
            "Жарнама шилтемесин жайгаштыруу үчүн **simbank** аркылуу 100 сом төлөп, чегин жөнөтүңүз.", 
            parse_mode="Markdown"
        )
        return

    # Издөө шилтемелерин даярдоо
    query_encoded = urllib.parse.quote(user_text)
    youtube_url = f"https://www.youtube.com/results?search_query={query_encoded}"
    music_url = f"https://www.youtube.com/results?search_query={query_encoded}+music"

    # Изоляцияланган баскычтар (Inline Keyboard)
    inline_markup = types.InlineKeyboardMarkup()
    btn_yt = types.InlineKeyboardButton("🎬 Видеону көрүү", url=youtube_url)
    btn_mus = types.InlineKeyboardButton("🎵 Музыкасын угуу", url=music_url)
    inline_markup.add(btn_yt)
    inline_markup.add(btn_mus)

    text = f"🔍 **Эсептелди:** '{user_text}' боюнча натыйжалар даяр!\n\nТөмөнкү баскычтардан каалаганыңызды тандаңыз:"
    bot.reply_to(message, text, parse_mode="Markdown", reply_markup=inline_markup)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)

import telebot
from telebot import types
import urllib.parse
import urllib.request
import json
import re

TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌍 Салам! Ыр издөө үчүн: **+ ырдын аты** деп жаз.\nМисалы: `+ белом самолете`", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.startswith('+'))
def find_song(message):
    query = message.text[1:].strip()
    if not query:
        bot.reply_to(message, "❌ Ырдын атын жазыңыз.")
        return

    msg = bot.reply_to(message, "⏳ Ырлар изделүүдө...")

    try:
        # YouTube ачык авто-издөө сурамы
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Видео ID жана аталыштарын бөлүп алуу
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        
        if not video_ids:
            bot.edit_message_text("❌ Эч нерсе табылган жок.", message.chat.id, msg.message_id)
            return

        # Бирдей чыккан видеолорду тазалоо (кайталанбашы үчүн)
        unique_ids = list(dict.fromkeys(video_ids))[:5]

        response_text = f"🎵 **'{query}' боюнча табылган ырлар:**\n\n"
        markup = types.InlineKeyboardMarkup()

        for i, vid in enumerate(unique_ids, 1):
            video_url = f"https://www.youtube.com/watch?v={vid}"
            response_text += f"{i}. Ырды көрүү/угуу #{i}\n"
            button = types.InlineKeyboardButton(f"▶️ {i}-ырды ачуу", url=video_url)
            markup.add(button)

        bot.edit_message_text(response_text, message.chat.id, msg.message_id, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.edit_message_text("⚠️ Издөөдө ката кетти. Кайра аракет кылып көрүңүз.", message.chat.id, msg.message_id)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()

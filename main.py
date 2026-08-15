import telebot
from telebot import types
import time

TOKEN = '8818539624:AAEaQcX4nMlwBp8ErlPKaTFPBegvUTQ8TSc'
CHANNEL_ID = '@kinoru_kgz'
bot = telebot.TeleBot(TOKEN)

# Катталууну текшерүү
def is_subscribed(user_id):
    try:
        # Бот каналда админ болушу шарт!
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Эгер статус төмөнкүлөрдүн бири болсо, демек катталган
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Ката: {e}")
        return False
    return False

# Издөө процесси
def perform_search(message, query):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    msg = bot.send_message(message.chat.id, "⏳ Издөөдө...")
    time.sleep(0.5)
    bot.edit_message_text("🔄 Табылууда...", message.chat.id, msg.message_id)
    time.sleep(0.5)

    link = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎵 Музыка", url=link))
    
    bot.edit_message_text(f"✅ **'{query}'** табылды:", message.chat.id, msg.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    # Эгер катталган болсо, түз эле саламдашат
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "👋 Салам! Мен даярмын. Каалаган ырды же видеону жазыңыз.")
    else:
        # Каттала элек болсо, баскычтарды чыгарат
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Каналга катталуу", url="https://t.me/kinoru_kgz"))
        markup.add(types.InlineKeyboardButton("✅ Катталдым", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ Ботту колдонуу үчүн биздин каналга катталыңыз:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Рахмат! Эми бот иштейт.")
        bot.edit_message_text("🎉 Рахмат! Эми каалаган нерсеңизди издей берсеңиз болот.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "⚠️ Сиз азырынча каналга каттала элексиз!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Катталган болсо - иштейт, жок болсо - катталууну сурайт
    if is_subscribed(message.from_user.id):
        perform_search(message, message.text)
    else:
        # Эгер катталбаса, кайра катталуу баскычын чыгарат
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Каналга катталуу", url="https://t.me/kinoru_kgz"))
        markup.add(types.InlineKeyboardButton("✅ Катталдым", callback_data="check_sub"))
        bot.reply_to(message, "⚠️ Издөө үчүн алгач каналга катталыңыз:", reply_markup=markup)

if __name__ == "__main__":
    bot.infinity_polling()

import telebot
from telebot import types
import time

# Сиздин токен
TOKEN = '8818539624:AAEaQcX4nMlwBp8ErlPKaTFPBegvUTQ8TSc'
CHANNEL_ID = '@kinoru_kgz'
bot = telebot.TeleBot(TOKEN)

# Катталууну текшерүү функциясы
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Издөө процессин аткаруучу функция
def perform_search(message, query):
    # Колдонуучунун жазган билдирүүсүн өчүрүү
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

# Баштоо командасы
@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "👋 Салам! Эми каалаган нерсеңизди издей берсеңиз болот.")
    else:
        ask_to_subscribe(message)

# Катталууга чакыруу билдирүүсү
def ask_to_subscribe(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Каналга катталуу", url="https://t.me/kinoru_kgz"))
    markup.add(types.InlineKeyboardButton("✅ Катталдым", callback_data="check_subscription"))
    bot.send_message(message.chat.id, "⚠️ Издөө үчүн алгач биздин каналга катталыңыз:", reply_markup=markup)

# Баскычтарды иштетүү (Callback Query)
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Рахмат! Сиз ийгиликтүү катталдыңыз.")
        bot.edit_message_text("🎉 Рахмат! Эми каалаган нерсеңизди издей берсеңиз болот.", call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "⚠️ Сиз азырынча каналга каттала элексиз!", show_alert=True)

# Негизги билдирүүлөрдү иштетүү
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if is_subscribed(message.from_user.id):
        perform_search(message, message.text)
    else:
        ask_to_subscribe(message)

if __name__ == "__main__":
    bot.infinity_polling()

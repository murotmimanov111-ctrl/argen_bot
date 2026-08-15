import telebot
from telebot import types
import time

TOKEN = '8819884297:AAEZKOJOzQv9BAVEpz36bDxhYZHbcV_Hpsc'
CHANNEL_ID = '@kinoru_kgz' # Каналдын username'и
bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Катталуу", url="https://t.me/kinoru_kgz")
    markup.add(btn)
    
    bot.send_message(message.chat.id, "👋 Салам! Ботту колдонуу үчүн алгач биздин каналга катталыңыз.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_search(message):
    user_id = message.from_user.id
    
    # 1. Катталууну текшерүү
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Каналга катталуу", url="https://t.me/kinoru_kgz"))
        bot.reply_to(message, "⚠️ Сиз каналга каттала элексиз! Издөө үчүн катталууңуз керек.", reply_markup=markup)
        return

    # 2. Издөө процесси
    search_query = message.text
    
    # Колдонуучунун жазган билдирүүсүн өчүрүү
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    # "Издөөдө..." билдирүүсү
    msg = bot.send_message(message.chat.id, "⏳ Издөөдө...")
    
    # "Анимация" (убакыт өткөрүү)
    time.sleep(1)
    bot.edit_message_text("🔄 Табылууда...", message.chat.id, msg.message_id)
    time.sleep(1)

    # 3. Натыйжаны көрсөтүү
    inline_markup = types.InlineKeyboardMarkup()
    # Бул жерде "Музыка" баскычы, аны басканда ырды угуу үчүн шилтеме
    link = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
    
    btn_music = types.InlineKeyboardButton("🎵 Музыка (угуу)", url=link)
    inline_markup.add(btn_music)
    
    bot.edit_message_text(f"✅ **'{search_query}'** табылды:", message.chat.id, msg.message_id, reply_markup=inline_markup, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()

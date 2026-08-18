import os
import time
import random
import threading
import schedule
import telebot
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = '8886843755:AAFmmGR7nEB3SsdLnxPNerzAm0pMskiuYLU'
CHANNEL_ID = '@kinoru_kgz'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"DEBUG: /start командасы келди: {message.from_user.id}") # Логго жазат
    try:
        reply_text = (
            "✨ *Арген, ты официально признан лучшим IT-специалистом!* 💻🚀\n\n"
            "Желаю тебе достигать новых невероятных высот, легко покорять "
            "любые вершины программирования и создавать самые крутые проекты! "
            "Пусть каждый твой код работает идеально, без единой ошибки. 💫🔥"
        )
        gif_url = "https://media.giphy.com/media/qgQUGGAC3P4vC/giphy.gif"
        
        bot.send_animation(
            chat_id=message.chat.id,
            animation=gif_url,
            caption=reply_text,
            parse_mode='Markdown'
        )
        print("DEBUG: Жооп жөнөтүлдү")
    except Exception as e:
        print(f"DEBUG: Жөнөтүүдө ката болду: {e}")

# ... (MESSAGES жана send_post функциясы мурдагыдай эле калат) ...
MESSAGES = ["🖤 *Твои глаза — мой самый любимый омут...*", "🏎 *Скорость в венах, ночные огни...*", "🤍 *Держи меня за руку крепче, чем прежде,*"]
KEYWORDS = ["bmw,m4,blackcar", "couples,kiss,romantic"]

def send_post():
    print("DEBUG: Каналга пост жөнөтүүгө аракет кылууда...")
    try:
        # (send_post ичиндеги мурунку коддоруңуз ошол бойдон калтырыңыз)
        keyword = random.choice(KEYWORDS)
        image_url = f"https://source.unsplash.com/800x1000/?{keyword}&sig={random.randint(1, 100000)}"
        bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=random.choice(MESSAGES), parse_mode='Markdown')
        print("DEBUG: Каналга пост ийгиликтүү жөнөтүлдү!")
    except Exception as e:
        print(f"DEBUG: Каналга жөнөтүүдө ката: {e}")

def start_polling():
    print("DEBUG: Бот Телеграмдан маалымат алууну баштады (polling)...")
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    threading.Thread(target=start_polling).start()
    
    schedule.every(1).hours.do(send_post)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

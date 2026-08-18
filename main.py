import os
import time
import random
import threading
import schedule
import telebot
from flask import Flask

# Render веб-сервери (Порт катасын болтурбоо үчүн)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Бот маалыматтары
TOKEN = '8886843755:AAFmmGR7nEB3SsdLnxPNerzAm0pMskiuYLU'
CHANNEL_ID = '@kinoru_kgz'

bot = telebot.TeleBot(TOKEN)

# 1. /start БАСКЫЧЫН БАСКАНДА ЖООП БЕРҮҮ (ЛИЧКАДА)
@bot.message_handler(commands=['start'])
def send_welcome(message):
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

# 2. КАНАЛГА СААТ САЙЫН ЖӨНӨТҮЛҮҮЧҮ ЭМОЦИОНАЛДУУ ЫР САРТАРЫ
MESSAGES = [
    "🖤 *Твои глаза — мой самый любимый омут...*\n\nВ них столько жизни, страсти и огня. 🥀\nИ если все на свете где-то тонут,\nТо я тону, смотря лишь на тебя. ✨",
    "🏎 *Скорость в венах, ночные огни...*\n\nВ этом городе мы с тобой одни. 🔥\nЧерный глянец, рев мотора и мост,\nДолетим до самых далеких звезд. ⚡️",
    "🤍 *Держи меня за руку крепче, чем прежде,*\n\nВ мире, где так мало искренней надежды. 🕊\nПусть вечер подарит тепло и покой,\nГлавное счастье — быть рядом с тобой. ✨",
    "🔥 *В её глазах — бушует океан,*\n\nА в его сердце — стиль и дикий характер. 🖤\nЛюбовь — это когда один взгляд\nЗаменяет тысячи лишних слов... 💞",
    "🌃 *Мы режем ночь по улицам пустым...*\n\nЗабыв про прошлый шум и дым. 🏎\nЛишь тишина, романтика и мы,\nСреди эстетики красивой темноты. ✨",
    "✨ *Не ищи идеалы, ищи душевный уют.* \n\nТу, с кем глаза без слов обо всем говорят. 🥀\nГде тебя ждут, любят и берегут, \nИ искренним взглядом встречает закат. ☕️",
    "🥀 *Взгляды, от которых замирает пульс...*\n\nСтрасть, которую невозможно скрыть. ❤️\nБыть рядом — лучший из всех чувств,\nУметь любить и истинно ценить. 💫",
    "🚘 *Шум мотора, тихий вечер, снег...*\n\nВ этом мире так важен свой человек. ❄️\nТот, чьи глаза горят для тебя,\nСогревая искренно и любя. ✨"
]

KEYWORDS = [
    "bmw,m4,blackcar",
    "couples,kiss,romantic",
    "darkcar,sportscar,night",
    "romantic,love,hug",
    "bmw,m5,snowcar"
]

def send_post():
    try:
        keyword = random.choice(KEYWORDS)
        image_url = f"https://source.unsplash.com/800x1000/?{keyword}&sig={random.randint(1, 100000)}"
        caption = random.choice(MESSAGES)
        
        bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'
        )
        print("Пост каналга ийгиликтүү жөнөтүлдү!")
    except Exception as e:
        print(f"Каналга жөнөтүүдө ката: {e}")

# Саат сайын жөнөтүү графиги
schedule.every(1).hours.do(send_post)

# 409 КОНФЛИКТ КАТАСЫН ЖОЮУЧУ ТАЗАЛООЧУ POLLING
def start_polling():
    try:
        bot.remove_webhook()
        time.sleep(1)
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Polling катасы: {e}")

if __name__ == '__main__':
    # Flask веб-серверин баштоо
    threading.Thread(target=run_flask).start()
    
    # Личкадагы /start буйругун угууну баштоо
    threading.Thread(target=start_polling).start()
    
    # Бот күйгөндө каналга дароо 1 пост жөнөтүү
    send_post()
    
    # Саат сайын кайталоочу цикл
    while True:
        schedule.run_pending()
        time.sleep(60)

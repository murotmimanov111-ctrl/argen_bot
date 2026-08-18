import os
import time
import random
import threading
import schedule
import telebot
from flask import Flask

# Render үчүн жасалма веб-сервер
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Сиздин бот токениңиз
TOKEN = '8886843755:AAFmmGR7nEB3SsdLnxPNerzAm0pMskiuYLU'
CHANNEL_ID = '@СИЗДИН_КАНАЛДЫН_ЮЗЕРНЕЙМИ'  # Каналыңыздын юзернейми

bot = telebot.TeleBot(TOKEN)

MESSAGES = [
    "✨ *Верь в себя и в свои возможности.* Каждый день — это новый шанс стать лучше! 💫",
    "🌿 *Позволь себе просто быть счастливым сегодня.* Маленькие шаги ведут к большим победам. ☕️",
    "☁️ *Красота вокруг нас, стоит только присмотреться.* Гармонии и уюта в ваш день! ☕️✨",
    "💭 *Не сравнивай свое начало с чьей-то серединой.* Твой путь уникален и прекрасен. 🌱",
    "🕊 *Пусть этот час принесет тебе спокойствие и вдохновение.* Улыбнись, все получится! ☀️",
    "🕯 *Создавай атмосферу, в которой тебе хочется жить.* Детали имеют значение. ✨",
    "⚡️ *Твоя энергия — твоя суперсила.* Направь ее на то, что действительно любишь! 🤍",
    "🌊 *Тишина и эстетика в каждом моменте.* Сделай паузу и просто подыши. ✨",
    "🌷 *Ты справляешься лучше, чем тебе кажется.* Верь в свой путь и не останавливайся! 💫",
    "☕️ *Маленькие радости делают день особенным.* Наслаждайся каждым мгновением. ✨"
]

def send_post():
    try:
        image_url = f"https://picsum.photos/800/1000?random={random.randint(1, 10000)}"
        caption = random.choice(MESSAGES)
        bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption,
            parse_mode='Markdown'
        )
        print("Пост ийгиликтүү жөнөтүлдү!")
    except Exception as e:
        print(f"Ката чыкты: {e}")

# График
schedule.every(1).hours.do(send_post)

if __name__ == '__main__':
    # Серверди өзүнчө потокто иштетүү
    threading.Thread(target=run_flask).start()
    
    # Дароо 1 пост жөнөтүү
    send_post()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

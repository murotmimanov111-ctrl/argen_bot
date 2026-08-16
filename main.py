import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = '8961768379:AAGVtgfAjWmJx_j7zVBGzhEipecDPZnXY5w'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салам, досум! 🌟🎶\nМага ырдын атын жазсаң, мен сага .mp3 файлын заматта жүктөп берем! 🔥💃")

@bot.message_handler(func=lambda message: True)
def download_and_send_audio(message):
    query = message.text
    status_msg = bot.reply_to(message, f"🥳 «{query}» ыры изделип жатат, азыр сизге mp3 файлын жүктөп жөнөтөм... 🎧✨")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1', # YouTube'дан биринчи чыккан ырды алат
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
        
        # Жүктөлгөн mp3 файлды жөнөтүү
        with open('song.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✨ Мына сиз каалаган ыр! Маанайыңыз сонун болсун! 🥰🎶")
        
        # Файлды серверден тазалоо жана маалымат билдирүүсүн өчүрүү
        os.remove('song.mp3')
        bot.delete_message(message.chat.id, status_msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"Кечириңиз, ырды жүктөөдө ката чыкты 😔 Кайра аракет кылып көрүңүз!", message.chat.id, status_msg.message_id)

bot.polling(none_stop=True)

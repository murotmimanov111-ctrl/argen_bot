import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = '8961768379:AAGVtgfAjWmJx_j7zVBGzhEipecDPZnXY5w'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Салам, досум! 🌟🎶\nМага ырдын атын жазсаң, мен сага аудио файлын заматта жүктөп берем! 🔥💃")

@bot.message_handler(func=lambda message: True)
def download_and_send_audio(message):
    query = message.text
    status_msg = bot.reply_to(message, f"🥳 «{query}» ыры изделип жатат, азыр сизге файлын жүктөп жөнөтөм... 🎧✨")
    
    # FFmpeg талап кылбаган жөнөкөй параметрлер
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': 'song.%(ext)s',
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info)
        
        # Жүктөлгөн аудио файлды жөнөтүү
        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✨ Мына сиз каалаган ыр! Маанайыңыз сонун болсун! 🥰🎶")
        
        # Файлды тазалоо жана статусту өчүрүү
        if os.path.exists(filename):
            os.remove(filename)
        bot.delete_message(message.chat.id, status_msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"Кечириңиз, ырды жүктөөдө ката чыкты 😔 Кайра аракет кылып көрүңүз!", message.chat.id, status_msg.message_id)

bot.polling(none_stop=True)

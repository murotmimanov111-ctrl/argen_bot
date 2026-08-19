import os
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8818539624:AAEaQcX4nMlwBp8ErlPKaTFPBegvUTQ8TSc"
JAMENDO_CLIENT_ID = "YOUR_JAMENDO_CLIENT_ID" # Өзүңүздүн Client ID жазасыз

app = Flask('')
@app.route('/')
def home(): return "Бот работает! 🚀"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Салам! Мен Argenдин музыкалык ботумун.\n\n"
        "Мага каалаган ырыңыздын атын жазыңыз, мен аны таап, сизге сураган форматыңызда жөнөтөм. 🎵"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if not query: return
    
    status = await update.message.reply_text("🔍 Издейм...")
    
    try:
        url = f"https://api.jamendo.com/v3.0/tracks/?client_id={JAMENDO_CLIENT_ID}&format=json&search={query}&limit=1"
        response = requests.get(url)
        data = response.json()
        
        tracks = data.get('results', [])
        if not tracks:
            await status.edit_text("❌ Ыр табылган жок.")
            return
            
        track = tracks[0]
        title = track.get('name', 'Музыка')
        artist = track.get('artist_name', 'Белгисиз')
        audio_url = track.get('audio')
        image_url = track.get('image')
        
        # YouTube'га түз издеп өтүүчү шилтеме
        youtube_search_url = f"https://www.youtube.com/results?search_query={artist}+{title}".replace(" ", "+")
        
        if audio_url:
            # Сиз каалаган тартипте текстти түзөбүз:
            # 1. Толук аталышы
            # 2. Юзериңиз
            # 3. YouTube шилтемеси жана текст
            caption = (
                f"🎵 **{artist} — {title}**\n\n"
                f"👤 @Argen\n\n"
                f"🔗 [YouTube'дан угуу]({youtube_search_url})"
            )
            
            # Биринчи фону (сүрөтү) кетет
            if image_url:
                await update.message.reply_photo(
                    photo=image_url,
                    caption=caption,
                    parse_mode="Markdown"
                )
            
            # Анан ылдыйында аудио файл кетет
            await update.message.reply_audio(
                audio=audio_url,
                title=title,
                performer=artist
            )
            await status.delete()
        else:
            await status.edit_text("❌ Аудио файл табылган жок.")
            
    except Exception as e:
        await status.edit_text("❌ Ката чыкты, кайра аракет кылыңыз.")

if __name__ == "__main__":
    Thread(target=run).start()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_bot.run_polling()

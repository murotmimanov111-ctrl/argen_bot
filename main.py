import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8817519388:AAH05Kz22gJ5bey4m-9p0TwiSmme7WGmnz4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Салам! Мен Argenдин музыкалык ботумун.\n\n"
        "Мага каалаган ырыңыздын атын жазыңыз, мен аны Deezer аркылуу таап, сизге жөнөтөм. 🎵"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if not query: return
    
    status = await update.message.reply_text("🔍 Издейм...")
    
    try:
        # Deezer API аркылуу издөө
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        data = response.json()
        
        tracks = data.get('data', [])
        if not tracks:
            await status.edit_text("❌ Ыр табылган жок.")
            return
            
        track = tracks[0]
        title = track.get('title', 'Музыка')
        artist = track.get('artist', {}).get('name', 'Белгисиз')
        audio_url = track.get('preview') # Deezer 30 секунддук же толук превью берет
        image_url = track.get('album', {}).get('cover_medium') # Альбомдун сүрөтү
        
        youtube_search_url = f"https://www.youtube.com/results?search_query={artist}+{title}".replace(" ", "+")
        
        if audio_url:
            caption = (
                f"🎵 **{artist} — {title}**\n\n"
                f"👤 @Argen\n\n"
                f"🔗 [YouTube'дан угуу]({youtube_search_url})"
            )
            
            if image_url:
                await update.message.reply_photo(
                    photo=image_url,
                    caption=caption,
                    parse_mode="Markdown"
                )
            
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
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Бот Deezer аркылуу иштеп жатат...")
    app_bot.run_polling()

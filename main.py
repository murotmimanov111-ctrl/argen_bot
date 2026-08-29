import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from yt_dlp import YoutubeDL

TOKEN = "8797849312:AAEMEvV-WydOdGwElCEzIH44MHpDhvYGmgw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# --- /START ---
@dp.message(F.text.casefold().in_(["/start", "start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 <b>Привет!</b> Отправь мне название любой песни (например: <i>Eminem Without Me</i>), и я найду её для тебя.",
        parse_mode="HTML"
    )

# --- МУЗЫКУ ИЗДӨӨ ЖАНА ЖӨНӨТҮҮ ---
@dp.message()
async def search_and_send_music(message: types.Message):
    if not message.text:
        return
        
    query = message.text.strip()
    if query.startswith("/"):
        return

    wait_msg = await message.answer("🔍 Ищу музыку, подождите...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': 'song_%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True
    }

    file_path = None
    try:
        def download():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                filename = ydl.prepare_filename(info)
                base, _ = os.path.splitext(filename)
                mp3_path = base + '.mp3'
                return info.get('title', 'Audio'), mp3_path

        loop = asyncio.get_running_loop()
        title, file_path = await loop.run_in_executor(None, download)

        if os.path.exists(file_path):
            audio_file = types.FSInputFile(file_path)
            await message.answer_audio(
                audio=audio_file, 
                caption=f"🎵 <b>{title}</b>",
                parse_mode="HTML"
            )
        else:
            await wait_msg.edit_text("❌ Не удалось найти файл песни.")
            return
        
        try:
            await wait_msg.delete()
        except Exception:
            pass

    except Exception as e:
        try:
            await wait_msg.edit_text("❌ Ошибка при поиске или скачивании песни. Попробуйте другой запрос.")
        except Exception:
            pass
    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

async def main():
    print("Музыкальный бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import telebot

# Токениңизди бул жерге туура коюңуз
TOKEN = '8976128121:AAG0hDOTLtbBUPdj1TQO8f5bilsXZ5sCegk'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎶 Салам! Мен Suno AI жардамчысымын.\n\nМага ырдын темасын же жанрын жаз, мен сага Suno AI үчүн даяр промпт түзүп берем.\n\nМисалы: 'кайгылуу махабат, рок стилинде'")

@bot.message_handler(func=lambda message: True)
def generate_prompt(message):
    topic = message.text
    
    # Suno AI үчүн профессионалдык калып
    prompt = f"""
✅ **Suno AI үчүн промпт:**

**Style/Genre:** {topic}
**Vibe:** Atmospheric, high quality, professional studio recording.

---
**Lyrics Template:**
[Verse 1]
(Бул жерге ырдын маанисине жараша ыр саптарын жазыңыз)

[Chorus]
(Бул жерге кайталанма бөлүгүн жазыңыз)

[Outro]
(Аяктоочу бөлүгү)
    """
    
    bot.reply_to(message, prompt, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()

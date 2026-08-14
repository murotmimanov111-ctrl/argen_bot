import telebot
from telebot import types

TOKEN = '8929956516:AAGUYLoszpYIUCBePNC0cqfMhMH1xkkcbnc'
bot = telebot.TeleBot(TOKEN)

# Колдонуучулардын абалын сактоо
user_stats = {}

def get_player(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {"hp": 100, "sword": False, "location": "start"}
    return user_stats[user_id]

# /start командасы
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.chat.id
    user_stats[user_id] = {"hp": 100, "sword": False, "location": "start"}
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🌲 Ойду карай басуу", callback_data="forest")
    btn2 = types.InlineKeyboardButton("🏰 Эски сепилге кирүү", callback_data="castle")
    markup.add(btn1, btn2)
    
    text = (
        "⚔️ **'Жоголгон Шаар' квестине кош келиңиз!**\n\n"
        "Сиз а сырдуу токойдун ортосунда ойгондуңуз. Колуңузда эч нерсе жок.\n"
        "Алдыңызда эки жол турат...\n\n"
        "❤️ **HP:** 100 | 🗡️ **Курал:** Жок\n\n"
        "Кайсы жолду тандайсыз?"
    )
    bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=markup)

# Интерактивдүү тандоолорду иштетүү
@bot.callback_query_handler(func=lambda call: True)
def game_logic(call):
    user_id = call.message.chat.id
    player = get_player(user_id)
    markup = types.InlineKeyboardMarkup()

    # 🌲 ТОКОЙ ЖОЛУ
    if call.data == "forest":
        player["sword"] = True
        btn = types.InlineKeyboardButton("🔙 Ийиниңизде кылыч менен артка кайтуу", callback_data="start_again")
        markup.add(btn)
        
        text = (
            "🌲 **Сиз токойго кирдиңиз.**\n\n"
            "Дарактын түбүнөн эски **Сыйкырдуу Кылыч** таап алдыңыз! 🗡️\n"
            "Инвентарыңызга кылыч кошулду.\n\n"
            f"❤️ **HP:** {player['hp']} | 🗡️ **Курал:** Бар"
        )
        bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # 🏰 СЕПИЛ ЖОЛУ
    elif call.data == "castle":
        if player["sword"]:
            # Эгер кылычы болсо — монстрду жеңет!
            btn = types.InlineKeyboardButton("🏆 Ажыдаарды издөө (Жеңиш)", callback_data="win")
            markup.add(btn)
            text = (
                "🏰 **Сепилдин ичинде каардуу Гоблин тосуп чыкты!**\n\n"
                "Бирок сиздин колуңузда **Кылыч** бар эле! Сиз Гоблинди бир сокку менен жеңдиңиз! ⚔️🔥\n\n"
                f"❤️ **HP:** {player['hp']} | 🗡️ **Курал:** Бар"
            )
        else:
            # Кылычы жок болсо — жаракат алат
            player["hp"] -= 40
            btn1 = types.InlineKeyboardButton("🌲 Качып чыгып токойго өтүү", callback_data="forest")
            btn2 = types.InlineKeyboardButton("🔄 Кайра баштоо", callback_data="start_again")
            markup.add(btn1, btn2)
            text = (
                "🏰 **Сепилге куралсыз кирдиңиз!**\n\n"
                "Каардуу Гоблин сизге кол салып, жаракат келтирди! (-40 HP) 💥\n\n"
                f"❤️ **HP:** {player['hp']} | 🗡️ **Курал:** Жок\n\n"
                "Жан соогалап качып чыгасызбы же жаңыдан баштайсызбы?"
            )
        bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # 🏆 ЖЕҢИШ
    elif call.data == "win":
        btn = types.InlineKeyboardButton("🎮 Жаңы оюн баштоо", callback_data="start_again")
        markup.add(btn)
        text = "🎉 **КУТТУКТАЙБЫЗ!** Сиз квестти ийгиликтүү аяктап, сепилди азат кылдыңыз!"
        bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # 🔄 КАЙРА БАШТОО
    elif call.data == "start_again":
        user_stats[user_id] = {"hp": 100, "sword": False, "location": "start"}
        btn1 = types.InlineKeyboardButton("🌲 Ойду карай басуу", callback_data="forest")
        btn2 = types.InlineKeyboardButton("🏰 Эски сепилге кирүү", callback_data="castle")
        markup.add(btn1, btn2)
        text = "⚔️ **Оюн кайра башталды.** Баштапкы абалга келдиңиз.\n\nКайсы жолду тандайсыз?"
        bot.edit_message_text(text, user_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

if __name__ == "__main__":
    print("RPG Бот ишке кирди...")
    bot.infinity_polling()

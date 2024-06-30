import telebot
from CODE import data_parsing
from add_tok import token
from add_tok import token_TG
# token = tokens['telegram_token']



token_VK=token
bot = telebot.TeleBot(token_TG)


@bot.message_handler(commands=["start"])
def send_help(message, token_VK):
    group_id=message.text[6:]
    try:
        new_people=data_parsing(group_id, token)
    except:
        bot.send_message(message.chat.id, message.text[5:] + "Не верный ID группы")

@bot.message_handler(commands=["help"])
def send(message):
    bot.send_message(message.chat.id, "/start + ID группы - программа пропарсит группу и выдаст новых её членов")



@bot.message_handler()
def info(message):
    bot.send_message(message.chat.id, "/help - для получения информации о работе бота")


bot.polling(none_stop=True)
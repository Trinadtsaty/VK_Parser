import time

import telebot
from Config import tokens
from CODE import data_parsing
from Config import find_params
from add_tok import token
from add_tok import token_TG
import pandas as pd
from datetime import date
import os


#
# token_VK = token
#
# find_params=find_params

token_TG="5308900440:AAFsI35w_esbY_RgtGmUf3fTbFLUTBphGgk"


bot = telebot.TeleBot(token_TG)

@bot.message_handler(commands=["dop_search"])
def dop_search(message):
    token_VK = token
    group_id=message.text[11:].split()
    print(group_id)

    for item in group_id:
        bot.send_message(message.chat.id, item)
        print(item)
        time.sleep(4)
        try:
            data_parsing(item, token_VK, find_params)
        except:
            bot.send_message(message.chat.id, message.text[11:] + " Не верный ID группы")

@bot.message_handler(commands=["start"])
def parse_data(message):
    group_mass=find_params["group_mass"]
    print(group_mass)
    token_VK = token
    for group in group_mass:
        print(group)
        bot.send_message(message.chat.id, group)
        time.sleep(4)
        try:
            data_parsing(group, token_VK, find_params)
        except:
            bot.send_message(message.chat.id, message.text[6:] + " Не верный ID группы")

@bot.message_handler(commands=["get_data"])
def get_data(message):
    new_file = "DB/" + date.today().strftime("%d_%m_%Y") + ".json"
    if not os.path.isfile(new_file):
        bot.send_message(message.chat.id, "Нет данных за сегодня")

    else:
        data = pd.read_json(new_file)
        data = data[data['GROUPS'].apply(len) > 0]

        for i in range(5):
            slice=data.iloc[i]
            slice_str = slice.to_string()
            bot.send_message(message.chat.id, slice_str)
        # slice = data[:5]
        #
        # slice_str = slice.to_string()
        # bot.send_message(message.chat.id, slice_str)



@bot.message_handler(commands=["help"])
def send(message):
    bot.send_message(message.chat.id, "/dop_search + ID группы - программа пропарсит группу и выдаст новых её членов \n можно вводить  несколько групп, через пробелы")
    bot.send_message(message.chat.id, "/start  - программа пропарсит заранее сохранённые группы, это займет какое-то время, ждите")
    bot.send_message(message.chat.id, "/get_data - программа выведит людей")


@bot.message_handler()
def info(message):
    bot.send_message(message.chat.id, "/help - для получения информации о работе бота")


bot.polling(none_stop=True)
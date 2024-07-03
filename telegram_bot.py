import time

import telebot
from CODE import data_parsing
from add_tok import find_params, token, token_TG
import pandas as pd
import os


#
# token_VK = token
#
# find_params=find_params
# token_TG="7380972075:AAEojzb18qqBOo2PFCLXbzAistjcixpeWIc"
# token_TG="5308900440:AAFsI35w_esbY_RgtGmUf3fTbFLUTBphGgk"


bot = telebot.TeleBot(token_TG)

@bot.message_handler(commands=["dop_search"])
def dop_search(message):
    token_VK = token
    group_id=message.text[11:].split()
    print(group_id)
    file_name="_"
    for item in group_id:
        if "file_name=" in item:
            file_name=item[10:]

    for item in group_id:
        if "file_name=" not  in item:
            bot.send_message(message.chat.id, "парсинг группы "+item)

            print(item)
            time.sleep(0.2)
            try:
                data_parsing(message, file_name, item, token_VK, find_params)
            except:
                bot.send_message(message.chat.id, "Ошибка в работе Бота")
    time.sleep(0.2)
    bot.send_message(message.chat.id, "Команда /dop_search завершила работу")

@bot.message_handler(commands=["start"])
def parse_data(message):
    file_name='_'
    group_mass=find_params["group_mass"]
    print(group_mass)
    token_VK = token
    for group in group_mass:
        print(group)
        bot.send_message(message.chat.id, "парсинг группы "+group)
        bot.send_message(message.chat.id, "бот уведомит о завершение работы")
        time.sleep(0.2)
        try:
            data_parsing(message, file_name, group, token_VK, find_params)
        except:
            bot.send_message(message.chat.id, "Ошибка в работе Бота")
    time.sleep(0.2)
    bot.send_message(message.chat.id, "Команда /start завершила работу")

@bot.message_handler(commands=["get_data"])
def get_data(message):

    message_a = message.text[9:].split()
    file_name="_"
    for item in message_a:
        if "file_name=" in item:
            file_name = item[10:]
            print(item)

    print(file_name)
    if file_name=="_":
        # new_file = "DB/" + date.today().strftime("%d_%m_%Y") + ".json"
        new_file='people_open.json'
        print(new_file)
    else:
        new_file = "DB/" + file_name + ".json"
        print(new_file)

    if not os.path.isfile(new_file):
        bot.send_message(message.chat.id, "Данного файла не существует")

    else:
        data = pd.read_json(new_file)
        data = data[data['GROUPS'].apply(len) > 0]

        if len(data)>=5:
            n=5
        else:
            n=len(data)

        print(n)
        for i in range(n):
            slice=data.iloc[i]
            fields=["ID","LINK","AGE","CITY"]
            slice=slice[fields]
            slice_str = slice.to_string()
            print(slice_str)
            bot.send_message(message.chat.id, slice_str, disable_web_page_preview=True)
        # slice = data[:5]
        #
        # slice_str = slice.to_string()
        # bot.send_message(message.chat.id, slice_str)
    time.sleep(0.2)
    bot.send_message(message.chat.id, "Команда /get_data завершила работу")



@bot.message_handler(commands=["help"])
def send(message):
    bot.send_message(message.chat.id, "<b>Любые действия с кодом занимают определённое время, бот уведомит вас по завершении работы</b>", parse_mode="html")
    bot.send_message(message.chat.id, "/dop_search + ID группы - программа пропарсит группу(ы).\nМожно вводить  несколько групп, через пробелы.\nПри вводе во время запроса \"file_name=*название файла, без пробелов*\" программа сохранит результаты работы в отдельный json файл")
    bot.send_message(message.chat.id, "/start  - программа пропарсит заранее сохранённые группы, это займет какое-то время, ждите")
    bot.send_message(message.chat.id, "/get_data - программа выведит людей.\nЕсли дополнительно передать аргумент \"file_name=*название файла, без пробелов*\" тогда программа, выдаст людей из нужного json файла")
    bot.send_message(message.chat.id, "/all_file - программа выдаёт название всех ранее сохранённых файлов")
    bot.send_message(message.chat.id, "/delete \"file_name=*название файла, без пробелов*\" удаляет указаный json файл\nПример: \"<code>/delete file_name=test</code>\"", parse_mode="html")
    bot.send_message(message.chat.id, "<b>При указании имени файла, не нужно укахывать расширение\n</b>Пример: \"<code>/get_data file_name=file1</code>\"", parse_mode="html")
    # bot.send_message(message.chat.id,
    #                  "/delete \"file_name=*название файла, без пробелов*\" удаляет указаный json файл\nПример: <pre>/delete file_name=test</pre>",
    #                  parse_mode="html")
    # bot.send_message(message.chat.id,
    #                  "<b>При указании имени файла, не нужно укахывать расширение\n</b>Пример: <pre>/get_data file_name=file1</pre>",
    #                  parse_mode="html")


@bot.message_handler(commands=["all_file"])
def all_file(message):

    if os.path.isdir("DB"):
        file=os.listdir("DB")
        if file==[]:
            bot.send_message(message.chat.id, "Файлы отсутсвуют")
        else:
            for item in file:
                bot.send_message(message.chat.id, item)
    else:
        bot.send_message(message.chat.id, "Файлы отсутсвуют")
    time.sleep(0.5)
    bot.send_message(message.chat.id, "Команда /all_file завершила работу")


@bot.message_handler(commands=["delete"])
def delete(message):
    message_a = message.text[7:].split()
    print(message_a)
    file_name="_"
    for item in message_a:
        if "file_name=" in item:
            file_name = item[10:]
            print(file_name)
    if file_name=="_":
        bot.send_message(message.chat.id, "Укажите название файла")
    else:
        new_file_name="DB/" + file_name + ".json"

        if not os.path.isfile(new_file_name):
            bot.send_message(message.chat.id, "Данного файла не существует")
        else:
            os.remove(new_file_name)
            bot.send_message(message.chat.id, "Файл "+file_name+" удалён")
    bot.send_message(message.chat.id, "Команда /delete завершила работу")


@bot.message_handler()
def info(message):

    bot.send_message(message.chat.id, "/help - для получения информации о работе бота")




bot.polling(none_stop=True)
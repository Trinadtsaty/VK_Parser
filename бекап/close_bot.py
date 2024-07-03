
import telebot
import codecs
import json
from datetime import date
import time
import numpy as np
import os
from add_tok import token_TG, find_params, token
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def request_zapros(url):
    retries = Retry(total=10, backoff_factor=0.2)
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    while True:
        try:
            req = requests.get(url)
            break
        except:
            pass
    src = req.json()
    print(src)
    posts = src["response"]["items"]
    time.sleep(0.26)
    return posts

def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates

def safe_json(name_js,file):
    f = codecs.open(f"{name_js}.json", "w", "utf_8")
    json.dump(file, f)
    f.close()

def glue_mass_people_close(group_id,token):
    offset =0
    mass1=[]
    while True:
        url = f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&offset={offset}&&access_token={token}&v=5.199"
        mass2 = request_zapros(url)
        if mass2!=[]:
            mass1=np.hstack([mass1, mass2])
            offset += 1000
        else:
            break
    return mass1

def parsing_close(token):
    football_groups="football_groups"
    people_close = "people_close"

    if not os.path.isfile("../people_close.json"):
        a = []
        safe_json(people_close, a)
        json_close = open_json("people_close.json")
    else:
        json_close = open_json("people_close.json")

    if not os.path.isfile("../football_groups.json"):
        a = []
        safe_json(football_groups, a)
        json_groups = open_json("football_groups.json")
    else:
        json_groups = open_json("football_groups.json")

    count_p=len(json_close)
    print("кол-во человек", count_p)
    count_g=len(json_groups)
    print("кол-во групп", count_g)
    form=count_g//4//60
    print("Приблиительное время работы бота: "+str(form)+" мин.")
    # bot.send_message(message.chat.id, "Приблиительное время работы бота: "+str(form)+" мин.")
    time.sleep(1)
    j = 0
    for group in json_groups:
        time_start = time.time()
        j += 1
        print("группа номер: ", j)


        humans = glue_mass_people_close(group["ID"], token)

        time_stop = time.time()
        print("время на выполнение:", "{:.2f}".format(time_stop - time_start), "сек.")
        k=0
        for people in json_close:
            k+=1
            print("Человек №",k)
            if people["ID"] in humans:
                gr = people.get("GROUPS",[])
                gr.append(group)
                people["GROUPS"]=gr






















time_start_1=time.time()
# print(time_start_1)
parsing_close(token)
print("время выполнения:", time.time()-time_start_1, "сек.")
import requests
import telebot
from add_tok import token
import codecs
import json
from datetime import date
import time
import numpy as np
import os
from add_tok import token_TG
from Config import find_params




bot = telebot.TeleBot(token_TG)


def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates

# Проверяем указан ли в дате год рождения, если да, вычисляем сколько лет человеку исполниться или исполнилось в этом году



def request_zapros(url):
    req = requests.get(url)
    src = req.json()
    posts = src["response"]["items"]
    time.sleep(0.2)
    return posts


def glue_mass_people(fields,group_id,token):
    offset =0
    mass1=[]
    while True:
        url = f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&offset={offset}&fields={fields}&access_token={token}&v=5.199"
        mass2 = request_zapros(url)
        if mass2!=[]:
            mass1=np.hstack([mass1, mass2])
            offset += 1000
        else:
            break
    return mass1
def filter_banned(posts):
    mass=[]
    for item in posts:
        try:
            banned = item["deactivated"]
        except:
            mass.append(item)
    return mass

def filter_sex(posts):
    mass=[]
    for item in posts:
        if item["sex"] == 2:
            mass.append(item)
    return mass


def filter_close(posts):
    open=[]
    close=[]
    for item in posts:
        if item["is_closed"]:
            close.append(item)
        else:
            open.append(item)
    return open, close

def filter_city(posts,ban_city):
    mass=[]
    for item in posts:
        city = item.get("city", {}).get("title","NaN")
        item["city"]=city
        if city  not in ban_city:
            mass.append(item)
    return mass

def filter_age(posts, filtre_age):
    mass=[]
    for item in posts:

        age=str(item.get("bdate", 0))
        if len(age)>=8:
            age=int(age[-4:])
            age=date.today().year-age
        else:
            age=0
        item["age"]=age

        if age<filtre_age:
            mass.append(item)
    return mass

def glue_mass_group(user_id, token, fields_group):
    offset = 0
    extended="1"
    mass1=[]
    while True:
        url = f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&offset={offset}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"
        mass2 = request_zapros(url)
        if mass2!=[]:
            mass1=np.hstack([mass1, mass2])
            offset += 1000
        else:
            break
    return mass1

def filter_gruops_deactivated(gruops):
    mass=[]
    for item in gruops:
        try:
            banned = item["deactivated"]
        except:
            mass.append(item)
    return mass
def filter_groups_page(gruops):
    mass=[]
    for item in gruops:
        if item["type"]=="page":
            mass.append(item)
    return mass

def filter_group_activity(gruops,ban_activity):
    mass=[]
    for item in gruops:
        if item["activity"] not in ban_activity:
            mass.append(item)
    return mass


def filter_group_close(gruops):
    mass=[]
    for item in gruops:
        if item["is_closed"] == 0:
            mass.append(item)
    return mass


def filter_group_keyword(gruops, football_keyword):
    mass=[]
    for item in gruops:
        name = item["name"]
        description = item["description"]
        if item["activity"]=="Футбол":
            mass.append(item)
        else:
            for teg in football_keyword:
                if (teg in name) or (teg in description):
                    mass.append(item)
                    break
    return mass


def user_from_group(name_j, group_id, token, ban_city, fields, filtre_age):
    json_open = open_json(f"{name_j}.json")
    mass_id=[]
    for item in json_open:
        mass_id.append(item["ID"])


    posts = glue_mass_people(fields, group_id, token)
    posts=filter_banned(posts)
    posts= filter_sex(posts)
    posts, close_posts = filter_close(posts)
    posts = filter_city(posts,ban_city)
    posts = filter_age(posts, filtre_age)

    for item in posts:
        id_a= item["id"]
        link="https://vk.com/id" + str(id_a)
        city=item["city"]
        age=item["age"]
        js_a = { "ID": id_a, "LINK": link, "CITY": city, "AGE": age}
        if js_a["ID"] not in mass_id:
            json_open.append(js_a)

    safe_json(name_j,json_open)


    return json_open

def groups_users(user_id, token, football_keyword, ban_activity, fields_group):
    group_mass = open_json("football_groups.json")
    append_js = []
    all_groups=[]

    gruops = glue_mass_group(user_id, token, fields_group)
    gr_all=gruops
    gruops = filter_gruops_deactivated(gruops)
    gr_all = filter_gruops_deactivated(gr_all)
    gruops = filter_groups_page(gruops)
    gr_all = filter_groups_page(gr_all)
    gruops = filter_group_activity(gruops, ban_activity)
    gruops = filter_group_keyword(gruops, football_keyword)
    for gruop in gr_all:
        id_a = gruop["id"]
        link = "https://vk.com/public" + str(id_a)
        name = gruop["name"]
        theme = gruop["activity"]
        data = {"ID": id_a, "LINK": link, "NAME": name, "theme": theme}
        all_groups.append(data)


    for gruop in gruops:
        id_a=gruop["id"]
        link = "https://vk.com/public" + str(id_a)
        name = gruop["name"]
        theme = gruop["activity"]
        data = {"ID": id_a, "LINK": link, "NAME": name, "theme":theme}
        if data not in group_mass:
            group_mass.append(data)
        append_js.append(data)
    f = codecs.open("football_groups.json", "w", "utf_8")
    json.dump(group_mass, f)
    f.close()
    return append_js, all_groups





def people_plus_groups(name_j, token, football_keyword, ban_activity,fields_group):
    people=open_json(f"{name_j}.json")
    j=0
    for item in people:
        j+=1
        print("number=",j)
        test=item.get("GROUPS", "NaN")
        if test=="NaN":
            try:
                user_id = item["ID"]
                js_a, js_gall=groups_users(user_id, token, football_keyword, ban_activity,fields_group)

                item["GROUPS"] = js_a
                item["ALL_GROUPS"] = js_gall
            except:
                print("error, restart")
                break

    return people





def run_parser(message, name_j, group_id, token, ban_city, fields, filtre_age, football_keyword, ban_activity, fields_group):
    try:
        user_from_group(name_j, group_id, token, ban_city, fields, filtre_age)
        tr=True
    except:
        print("Не удалось получить информацию о пользователях")
        bot.send_message(message.chat.id, message.text[11:] + " Не верный ID группы")
        tr=False
    json_open = open_json(f"{name_j}.json")

    n=len(json_open)
    print(n)
    time.sleep(2)

    for i in range(n//8):
        print("i=", i)
        js_gr = people_plus_groups(name_j, token, football_keyword, ban_activity,fields_group)
        safe_json(name_j,js_gr)
    if tr:
        bot.send_message(message.chat.id, "Группа " + group_id + " пропаршена")
    json_open = open_json(f"{name_j}.json")
    return json_open

def safe_json(name_js,file):
    f = codecs.open(f"{name_js}.json", "w", "utf_8")
    json.dump(file, f)
    f.close()


def data_parsing(message, name_file, group_id, token, find_params):

    fields_group = find_params["fields_groups"]
    fields = find_params["fields"]
    ban_city = find_params["ban_city"]
    football_keyword = find_params["football_keyword"]
    filtre_age = find_params["filtre_age"]
    ban_activity = find_params["ban_activity"]
    if not os.path.isdir("DB"):
        os.mkdir("DB")
    if name_file=="_":
        day = "DB/" + date.today().strftime("%d_%m_%Y")
        if not os.path.isfile(f"{day}.json"):
            a=[]
            safe_json(day,a)
    else:
        day="DB/" + name_file
        if not os.path.isfile(f"{day}.json"):
            a = []
            safe_json(day, a)

    new_json=run_parser(message, day, group_id, token, ban_city, fields, filtre_age, football_keyword, ban_activity, fields_group)
    if not os.path.isfile("people_open.json"):
        a = []
        safe_json("people_open", a)

    index_json=open_json("people_open.json")
    new_people=[]
    index_json_id = []

    for item in index_json:
        index_json_id.append(item["ID"])
    for item in new_json:
        if item["ID"] not in index_json_id:
            new_people.append(item)
            index_json.append(item)

    safe_json("people_open",index_json)
    return new_people


# name="people_open"
fields_group = "activity,deactivated,description,is_closed"
group_id="footballpremierleague_hse"
#group_id="222824253"
fields = "sex,is_closed,city,bdate,deactivated"
ban_city=["Санкт-Петербург"]
football_keyword=["Football","Футбол","Football","ФУТБОЛ","FOOTBALL","футбол","football", "ФК", "фк"]
group_teg=["Спортивная команда", "Спортивная организация", ""]
filtre_age=1000000
ban_activity=""
# name="people_open_with_groups.json"


# group_id="222824253"
# templates=data_parsing(group_id, token, find_params)
# # j=0
# # for i in templates:
# #     j+=1
# #     print(j, i)


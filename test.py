
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





bot = telebot.TeleBot(token_TG)


def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates

# Проверяем указан ли в дате год рождения, если да, вычисляем сколько лет человеку исполниться или исполнилось в этом году



def request_zapros(url):
    retries = Retry(total=10, backoff_factor=0.2)
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
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


def safe_json(name_js,file):
    f = codecs.open(f"{name_js}.json", "w", "utf_8")
    json.dump(file, f)
    f.close()
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


    safe_json(name_j, json_open)


    return json_open


fields_group = find_params["fields_groups"]
fields = find_params["fields"]
ban_city = find_params["ban_city"]
football_keyword = find_params["football_keyword"]
filtre_age = find_params["filtre_age"]
ban_activity = find_params["ban_activity"]
name_j="DB/"+"all_people"
group_id="25205856"

user_from_group(name_j, group_id, token, ban_city, fields, filtre_age)


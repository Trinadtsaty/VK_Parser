import requests
from add_tok import token
import codecs
import json
import datetime
from datetime import date
import time
import numpy as np




# Создаём необходимые json файлы для дальнейшей работы с ними
# f = open("people.json", "w")
# f.close()
# f = open("football_groups.json", "w")
# f.close()

def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates

# Проверяем указан ли в дате год рождения, если да, вычисляем сколько лет человеку исполниться или исполнилось в этом году



def request_zapros(url):
    req = requests.get(url)
    src = req.json()
    posts = src["response"]["items"]
    return posts

def serch_close(user_id, group_id, token):
    url_user_from_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&access_token={token}&v=5.199"
    people=request_zapros(url_user_from_group)
    if int(user_id) in people:
        return True
    else:
        return False

def zapr_mass(file,zapr):
    a=[]
    for item in file:
        if item[zapr] not in a:
            a.append(item[zapr])
    return a

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
    g=0
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


def user_from_group(group_id, token, ban_city, fields, filtre_age):
    json_open = []
    json_close = []
    j = 0
    k=0

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
        j+=1
        js_a={"NUMBER":j,"ID": id_a, "LINK": link, "CITY": city, "AGE": age}
        json_open.append(js_a)

    for item in close_posts:
        id_a = item["id"]
        link = "https://vk.com/id" + str(id_a)
        k+=1
        js_a = {"NUMBER":k,"ID": id_a, "LINK": link, "CITY": "NaN", "AGE": "NaN"}
        json_close.append(js_a)

    return json_open, json_close

def groups_users(user_id, token, football_keyword, ban_activity):
    group_mass = open_json("football_groups.json")
    append_js = []

    gruops = glue_mass_group(user_id, token, fields_group)
    gruops = filter_gruops_deactivated(gruops)
    gruops = filter_groups_page(gruops)
    gruops = filter_group_activity(gruops, ban_activity)
    gruops = filter_group_keyword(gruops, football_keyword)

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
    return append_js
    # time.sleep(0.2)




def people_plus_groups(name, token, football_keyword, ban_activity):
    people=open_json(name)
    for item in people:
        test=item.get("GROUPS", [])
        if test==[]:
            user_id=item["ID"]
            user_id = item["ID"]
            js_a=groups_users(user_id, token, football_keyword, ban_activity)
            item["GROUPS"] = js_a

    return people





















fields_group = "activity,deactivated,description,is_closed"
group_id="footballpremierleague_hse"
fields = "sex,is_closed,city,bdate,deactivated"
ban_city=[""]
football_keyword=["Football","Футбол","Football","ФУТБОЛ","FOOTBALL","футбол","football", "ФК", "фк"]
group_teg=["Спортивная команда", "Спортивная организация", ""]
filtre_age=1000000
ban_activity=""
name="people_open.json"

# js_open, js_close = user_from_group(group_id, token, ban_city, fields, filtre_age)


# f = codecs.open("people_open.json", "w", "utf_8")
# json.dump(js_open, f)
# f.close()
#
# f = codecs.open("people_close.json", "w", "utf_8")
# json.dump(js_close, f)
# f.close()


js_gr = people_plus_groups(name, token, football_keyword, ban_activity)

f = codecs.open("people_open_with_groups.json", "w", "utf_8")
json.dump(js_gr, f)
f.close()
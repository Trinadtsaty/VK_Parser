import json
import pandas
import requests
import codecs
import numpy as np
import datetime
from datetime import datetime
# with open('people.json') as f:
    # templates = f.read()
# templates=pandas.read_json("people.json")
# for item in templates:
#     # if item["banned"] !=None:
#     print(item.head())

#
# print(templates.head())

# data_now = datetime.now()
# data_now = str(datetime.now())[:4]
# print(data_now)

# with open('people.json') as f:
#     templates = json.load(f)

# for item in templates:
    # print(item["banned"])


# group_id=""
from add_tok import token

# def user_from_group(group_id, token):
#     # Загружаем JSON файл, с пользователями группы
#     json_per = []
#     fields = "first_name,last_name"
#     url_user_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&fields={fields}&access_token={token}&v=5.199"
#     req = requests.get(url_user_group)
#     src = req.json()
#     posts = src["response"]["items"]
#     for item in posts:
#         try:
#             first_name=item["first_name"]
#             last_name=item["last_name"]
#             if first_name=="Семён" and last_name=="Ермаков":
#                 id = item["id"]
#                 link = "https://vk.com/id" + str(id)
#                 data=group_users(id, token)
#                 json_per.append(
#                     {"ID": id, "LINK": link, "groups":data}
#                 )
#         except:
#             continue
#
#     return json_per


# football_teg=["Football","Футбол","Football","ФУТБОЛ","FOOTBALL","футбол","football"]
group_teg=["Спортивный клуб","Футбол", "Спортивная организация", "Спортивная команда", "Футбольная команда"]
# user_id=""
# def group_users(user_id, token,football_teg):
#     f = codecs.open("football_groups.json", "r", "utf_8")
#     group_mass=json.load(f)
#     f.close()
#     append_js=[]
#     extended = "1"
#     # https: // dev.vk.com / ru / reference / objects / group - документация по фильтрам
#     fields_group = "activity,deactivated,description,is_closed"
#     url_user_group = f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"
#     req = requests.get(url_user_group)
#     src = req.json()
#     gruops = src["response"]["items"]
#
#     for gruop in gruops:
#         try:
#             work=gruop["deactivated"]
#             continue
#         except:
#             theme = gruop["activity"]
#             if theme=="Футбол":
#                 id=gruop["id"]
#                 link = "https://vk.com/public" + str(id)
#                 name=gruop["name"]
#                 data={"ID":id, "LINK":link, "NAME":name}
#                 group_mass.append(data)
#                 append_js.append(data)
#
#             else:
#                 name = gruop["name"]
#                 description=gruop["description"]
#                 for teg in football_teg:
#                     if (teg in name) or (teg in description):
#                         id = gruop["id"]
#                         link = "https://vk.com/public" + str(id)
#                         name = gruop["name"]
#                         data = {"ID": id, "LINK": link, "NAME": name, "theme":theme}
#                         group_mass.append(data)
#                         append_js.append(data)
#                     else:
#                         continue
#
#
#
#
#     f = codecs.open("football_groups.json", "w", "utf_8")
#     json.dump(group_mass, f)
#     f.close()
#     return append_js



# with codecs.open('people.json', "r", "utf_8") as f:
#     templates = json.load(f)
# for i in templates:
#     print(i)

# with codecs.open('football_groups.json', "r", "utf_8") as f:
#     templates = json.load(f)
# a=[]
# for i in templates:
#     if i["theme"] not in a:
#         a.append(i["theme"])
# print(a)
# with codecs.open('people.json', "r", "utf_8") as f:
#     templates = json.load(f)
# for i in templates:
#     print(i)

def zapr_mass(file,zapr):
    a=[]
    for item in file:
        if item[zapr] not in a:
            a.append(item[zapr])
    return a
def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates

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

def all_search(name1,name2,token):
    new_spisok=[]
    gruops=open_json(name1)
    peoples=open_json(name2)
    for people in peoples:
        for group in gruops:
            if serch_close(people["ID"], group["ID"], token):
                a=people["GROUPS"]
                a.append(group)
                people["GROUPS"]=a


def glue_mass(fields,group_id,token):
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

def user_from_group(group_id, token):
    # Загружаем JSON файл, с пользователями группы
    json_per = []
    posts=[]
    j=0
    offset = 0
    fields = "sex,is_closed,city,bdate,deactivated"
    posts=glue_mass(fields,group_id,token)

    # Идёт циклом по каждому пользователю
    for item in posts:
        # Получаем статус пользователя (отфильтровываем забаненные или удалённые страницы)
        id = item["id"]
        link = "https://vk.com/id" + str(id)
        try:
            time = item["deactivated"]
            j += 1
            json_a = {"NUMBER": j, "ID": id, "LINK": link, "CLOSE": time, "SEX":"ban"}
            json_per.append(json_a)
        except:
            time=item["is_closed"]
            sex=item["sex"]
            try:
                age=item["bdate"]
            except:
                age="NaN"

            j += 1
            json_a = {"NUMBER": j, "ID": id, "LINK": link, "CLOSE": time, "SEX":sex, "AGE": age}
            json_per.append(json_a)


    return json_per

# group_id="footballpremierleague_hse"
# f = codecs.open("people12.json", "w", "utf_8")
# json.dump(user_from_group(group_id, token), f)
# f.close()
#
with codecs.open('people_close.json', "r", "utf_8") as f:
    templates = json.load(f)
for i in templates:
    print(i)

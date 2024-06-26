import requests
from add_tok import token
import codecs
import json
import datetime
from datetime import datetime
import time

group_id="footballpremierleague_hse"
# group_id="ultdank"
#
count=100
fields="sex"
fields_group="activity"
extended="1"
football_teg=["Football","Футбол","Football","ФУТБОЛ","FOOTBALL","футбол","football", "ФК", "фк"]
group_teg=["Спортивная команда", "Спортивная организация", ""]

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
def age_read(age):
    if (len(age) >= 8) and age != "НЕ УКАЗАНО":
        age = int(age[len(age) - 4:])
        data_now = int(str(datetime.now())[:4])

        age = str(data_now - age)
    else:
        age = "НЕ УКАЗАНО"
    return age
def city(city):
    pass

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

def user_from_group(group_id, count, token,football_teg):
    # Загружаем JSON файл, с пользователями группы
    json_per = []
    fields = "sex,is_closed,city,bdate,deactivated"
    url_user_from_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&count={count}&fields={fields}&access_token={token}&v=5.199"

    posts = request_zapros(url_user_from_group)

    # Идёт циклом по каждому пользователю
    for item in posts:
        # Получаем статус пользователя (отфильтровываем забаненные или удалённые страницы)
        try:
            banned = item["deactivated"]
        except:
            banned = None

        if banned=="banned" or banned=="deleted":
            continue

        else:

            # Фильтруем женщин, 1 - пользователь женщина
            if item["sex"] == 1:
                continue

            else:
                id = item["id"]
                link = "https://vk.com/public" + str(id)

                # Проверяем закрытый ли у пользователя профиль, где True - закрытый
                open_close = item["is_closed"]

                if open_close:
                    # Записываем json строку, если профиль - закрытый
                    json_per.append(
                        {"ID": id, "LINK": link, "CLOSE": open_close, "CITY": "НЕ УКАЗАНО", "AGE": "НЕ УКАЗАНО", "GROUPS": "НЕ УКАЗАНО"}
                    )
                else:

                    # получаем даду рождения пользователя
                    try:
                        age = str(item["bdate"])
                    except:
                        age="НЕ УКАЗАНО"


                    age=age_read(age)


                    # Узнаём указанный город
                    try:
                        city=item["city"]["title"]
                    except:
                        city="НЕ УКАЗАНО"

                    # Записываем файл в массив с json строками
                    data = group_users(id, token, football_teg)
                    if data==[]:
                        data="Сообщества скрыты"
                    json_per.append({"ID": id, "LINK": link, "CLOSE": open_close, "CITY": city, "AGE": age, "GROUPS": data})

                # Собираем группы, на которые подписан пользователь



    return json_per


# Функция по получению сообществ на которые подписан пользователь
def group_users(user_id, token, football_teg):
    # копируем содержимое json файла с сообществами на футбольную тематику в массив
    group_mass=open_json("football_groups.json")

    # Создаём массив для записи групп пользователя
    append_js=[]

    # Фильтр для запроса, показывает вместе страницы и группы, что упрощает вызов информации о них
    extended = "1"
    # https: // dev.vk.com / ru / reference / objects / group - документация по фильтрам
    fields_group = "activity,deactivated,description,is_closed"

    url_groups_user = f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"

    # У ВК стоит ограничение на 5 запросов в секунду, строчка наобходима чтобы соответсвовать ему
    time.sleep(0.2)
    gruops = request_zapros(url_groups_user)

    # Идёт в цикле по всем подпискам пользователя
    for gruop in gruops:
        # Проверяем работает ли группа
        try:
            work=gruop["deactivated"]
            continue
        except:
            # Отфильтровываем страницы от групп
            if gruop["type"] == "page":

                # Проверяем тему сообщества, если она Футбол, то записываем группу
                theme = gruop["activity"]
                if theme=="Футбол":
                    id=gruop["id"]
                    link = "https://vk.com/public" + str(id)
                    name=gruop["name"]
                    data={"ID":id, "LINK":link, "NAME":name, "theme":"Футбол"}
                    # Проверяем нет ли повторяющихся сообществ
                    if data not in group_mass:
                        group_mass.append(data)

                    append_js.append(data)

                # Если тема не футбол, проверяем ключевые слова в загаловки сообщества, а так же в описании
                else:
                    name = gruop["name"]
                    description=gruop["description"]

                    # Идём в цикле по тегам
                    for teg in football_teg:
                        if (teg in name) or (teg in description):
                            id = gruop["id"]
                            link = "https://vk.com/public" + str(id)
                            name = gruop["name"]
                            data = {"ID": id, "LINK": link, "NAME": name, "theme":theme}
                            # Проверяем нет ли повторяющихся сообществ
                            if data not in group_mass:
                                group_mass.append(data)
                            append_js.append(data)
                        else:
                            continue



    # Записываем найденный сообщества по футболу в json файл
    f = codecs.open("football_groups.json", "w", "utf_8")
    json.dump(group_mass, f)
    f.close()
    return append_js


f = codecs.open("people.json", "w", "utf_8")
json.dump(user_from_group(group_id, count, token,football_teg), f)
f.close()
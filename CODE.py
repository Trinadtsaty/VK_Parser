import requests
from add_tok import token
import codecs
import json
import datetime
from datetime import datetime

group_id="footballpremierleague_hse"
# group_id="ultdank"
#
count=100
fields="sex"
fields_group="activity"
extended="1"
football=["football","Футбол"]

def user_from_group(group_id, count, token):
    # Загружаем JSON файл, с пользователями группы
    json_per = []
    fields = "sex,is_closed,city,bdate,deactivated"
    url_user_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&count={count}&fields={fields}&access_token={token}&v=5.199"
    req = requests.get(url_user_group)
    src = req.json()
    posts = src["response"]["items"]

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

            # Фильтруем женщин
            if item["sex"] == 1:
                continue

            else:
                id = item["id"]
                link = "https://vk.com/id" + str(id)

                # Проверяем закрытый ли у пользователя профиль, где True - закрытый
                open_close = item["is_closed"]

                if open_close:
                    # Записываем json строку, если профиль - закрытый
                    json_per.append(
                        {"ID": id, "LINK": link, "CLOSE": open_close, "CITY": "НЕ УКАЗАНО", "AGE": "НЕ УКАЗАНО"}
                    )
                else:

                    # получаем даду рождения пользователя
                    try:
                        age = str(item["bdate"])
                    except:
                        age="НЕ УКАЗАНО"

                    # Проверяем указан ли в дате год рождения, если да, вычисляем сколько лет человеку исполниться или исполнилось в этом году
                    if (len(age) >= 8) and age!="НЕ УКАЗАНО":
                        age = int(age[len(age) - 4:])
                        data_now = int(str(datetime.now())[:4])
                        age = str(data_now - age)
                    else:
                        age="НЕ УКАЗАНО"

                    # Узнаём указанный город
                    try:
                        city=item["city"]["title"]
                    except:
                        city="НЕ УКАЗАНО"

                # Записываем файл в массив с json строками
                json_per.append({"ID": id, "LINK": link, "CLOSE": open_close, "CITY": city, "AGE": age})

                # Собираем группы, на которые подписан пользователь



    return json_per



def group_users(user_id, token):
    extended = "1"
    fields_group = "activity"
    url_user_group=f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"
    req = requests.get(url_user_group)
    src = req.json()
    posts = src["response"]["items"]


f = codecs.open("people.json", "w", "utf_8")
json.dump(user_from_group(group_id, count, token), f)
f.close()
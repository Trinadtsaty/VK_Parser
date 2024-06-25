import requests
from add_tok import token
import codecs
import json
import datetime
from datetime import datetime

group_id="footballpremierleague_hse"
#
count=20
fields="sex"
fields_group="activity"
extended="1"


def user_from_group(group_id, count, token):
    json_per = []
    fields = "sex,is_closed,city,bdate"
    url_user_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&count={count}&fields={fields}&access_token={token}&v=5.199"
    req = requests.get(url_user_group)
    src = req.json()
    posts = src["response"]["items"]
    for item in posts:
        try:
            if item["sex"] == 1:
                continue
            else:
                link = "https://vk.com/id" + str(item["id"])
                id = item["id"]
                open_close=item["is_closed"]
                if open_close:
                    age = 0
                    json_per.append({"ID": id, "LINK": link, "CLOSE": open_close, "CITY": "НЕ УКАЗАНО", "AGE": "НЕ УКАЗАНО"})
                else:
                    age=str(item["bdate"])
                    if len(age)>=8:
                        age=int(age[len(age)-4:])
                        data_now = int(str(datetime.now())[:4])
                        age=str(data_now-age)

                    else:
                        age="НЕ УКАЗАНО"
                    city=item["city"]["title"]
                    json_per.append({"ID": id, "LINK": link, "CLOSE": open_close, "CITY": city, "AGE": age})
        except:
            continue
    return json_per
def group_users(user_id, token):
    extended = "1"
    fields_group = "activity"
    url_group=f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"
    req = requests.get(url_user_group)
    src = req.json()
    posts = src["response"]["items"]


f = codecs.open("people.json", "w", "utf_8")
json.dump(user_from_group(group_id, count, token), f)
f.close()
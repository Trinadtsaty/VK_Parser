import requests
from tok import token
import codecs

group_id="footballpremierleague_hse"
#
count=20
fields="sex,domain"


url=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&count={count}&fields={fields}&access_token={token}&v=5.199"

# url=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&sort={sort}&count={count}&fields={fields}&access_token={token}&v=5.199"
f=codecs.open("PEOPLE.JSON", "w", "utf_8_sig")
f.close()
req=requests.get(url)
src=req.json()
posts=src["response"]["items"]
for item in posts:
    try:
        if item["sex"]==1:
            continue
        else:

            print(item["id"])
            print(item["sex"])
            print(item["domain"])
    except:
        continue

# f = codecs.open("PEOPLE.JSON", "a", "utf_8_sig")
# f.write(str({"123":"id"+item["id"]}))
# f.close()

# users.getSubscriptions
# src=req.json
# ID_user=src["response"]["items"]
# print(req.text)
# print(ID_user)

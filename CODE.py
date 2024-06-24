import requests
from tok import token
import codecs
import json

group_id="footballpremierleague_hse"
#
count=20
fields="sex"


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
            link="https://vk.com/id"+str(item["id"])
            id=item["id"]
            json_per='{"'+str(id)+'":"'+link+'"}'

    except:
        continue


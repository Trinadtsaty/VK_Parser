import requests
from add_tok import token
import codecs
import json

group_id="footballpremierleague_hse"
#
count=20
fields="sex"
fields_group="activity"
# user_id=""
extended="1"
url_user_group=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&count={count}&fields={fields}&access_token={token}&v=5.199"
url_group=f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"

# url_group=f"https://api.vk.com/method/users.getSubscriptions?user_id={user_id}&extended={extended}&fields={fields_group}&access_token={token}&v=5.199"
# url=f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&sort={sort}&count={count}&fields={fields}&access_token={token}&v=5.199"

# f=codecs.open("PEOPLE.JSON", "w", "utf_8_sig")
# f.close()
# f=codecs.open("PEOPLE.JSON", "a", "utf_8_sig")
req=requests.get(url_user_group)
src=req.json()
posts=src["response"]["items"]
for item in posts:
    try:
        if item["sex"]==1:
            continue
        else:
            link="https://vk.com/id"+str(item["id"])
            id=item["id"]
            # json_per='{"'+str(id)+'":"'+link+'"}'+"\n"
            json_per = '{"ID" : "' + str(id) + '"' + ' ,"link" : ' +link+'"}' + "\n"
            f = codecs.open("PEOPLE.JSON", "a", "utf_8_sig")
            f.write(json_per)
            f.close()
    except:
        continue


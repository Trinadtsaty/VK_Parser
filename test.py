import requests
import telebot
import codecs
import json
from datetime import date
import time
import numpy as np
import os
from add_tok import token_TG, find_params, token

def request_zapros(url):
    req = requests.get(url)
    src = req.json()
    print(src)
    posts = src["response"]["items"]
    time.sleep(0.21)
    return posts

def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates


def glue_mass_people_close(group_id,token):
    offset =0
    mass1=[]
    while True:
        url = f"https://api.vk.com/method/groups.getMembers?group_id={group_id}&offset={offset}&&access_token={token}&v=5.199"
        mass2 = request_zapros(url)
        if mass2!=[]:
            mass1=np.hstack([mass1, mass2])
            offset += 1000
        else:
            break
    return mass1

def safe_json(name_js,file):
    f = codecs.open(f"{name_js}.json", "w", "utf_8")
    json.dump(file, f)
    f.close()



group_id="75099129"


time_start=time.time()
a=glue_mass_people_close(group_id,token)
print("время выполнения:", time.time()-time_start, "сек.")
print(a[1])

# HTTPSConnectionPool(host='api.vk.com', port=443): Max retries exceeded with url: /method/groups.getMembers?group_id=75099129&offset=6000&&access_token=*мой_токен*&v=5.199 (Caused by SSLError(SSLError(1, '[SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC] decryption failed or bad record mac (_ssl.c:1125)')))

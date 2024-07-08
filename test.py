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


def safe_json(name_js,file):
    f = codecs.open(f"{name_js}.json", "w", "utf_8")
    json.dump(file, f)
    f.close()

def open_json(name):
    with codecs.open(name, "r", "utf_8") as f:
        templates = json.load(f)
    return templates


# a=open_json("people_open.json")
# # a=open_json("DB/all_people.json")
# a=open_json("DB_n/04_07_2024.json")
# print(len(a))
# #
# safe_json("DB/all_people",a)

import datetime

current_time = datetime.datetime.now().time()
print(current_time)
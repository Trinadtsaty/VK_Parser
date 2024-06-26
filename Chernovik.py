import json
import pandas
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

with open('people.json') as f:
    templates = json.load(f)

# for item in templates:
    # print(item["banned"])
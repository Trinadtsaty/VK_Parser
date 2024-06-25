import json
import pandas
import datetime
from datetime import datetime
# with open('people.json') as f:
    # templates = f.read()
templates=pandas.read_json("people.json")

print(templates)

# data_now = datetime.now()
# data_now = str(datetime.now())[:4]
# print(data_now)
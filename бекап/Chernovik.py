import json
import pandas
import requests
import codecs
import numpy as np
import datetime
from datetime import datetime, date
#
with codecs.open('DB/29_06_2024.json', "r", "utf_8") as f:
    templates = json.load(f)
    j=0
for i in templates:
    j+=1
    print(j, i)

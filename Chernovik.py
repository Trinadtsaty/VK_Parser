import json
import pandas
import requests
import codecs
import numpy as np
import datetime
from datetime import datetime

with codecs.open('people_open.json', "r", "utf_8") as f:
    templates = json.load(f)
    j=0
for i in templates:
    j+=1
    print(j, i)



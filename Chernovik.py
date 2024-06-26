import json
import pandas
import requests
import codecs
import numpy as np
import datetime
from datetime import datetime

with codecs.open('people_close.json', "r", "utf_8") as f:
    templates = json.load(f)
for i in templates:
    print(i)



import json
import codecs



with codecs.open('groups_all.json', "r", "utf_8") as f:
    templates = json.load(f)
    j=0
for i in templates:
    j+=1
    print(j, i)
import json


with open('bible.json') as json_file:
    data = json.load(json_file)

print(data['Joshua'][str(1)][str(6)].strip('\"\''))
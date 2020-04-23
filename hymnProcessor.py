import json 

with open('./hymn_numbered.json') as f:
    items = json.load(f)

# search for given hymn number
def search(num):
    for item in items:
        if item['hymnNumber'] == num:
            print(item)


search(10)

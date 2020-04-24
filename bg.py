# background selector 
import json, random

with open('background.json') as jsonFile:
    data = json.load(jsonFile)

def findRandomImg():
    rnum = random.randint(0, 2)

    if rnum == 0:
        return (random.choice(data['Birds']))
    elif random == 1:
        return (random.choice(data['Nightsky']))
    else:
        return (random.choice(data['Sky']))


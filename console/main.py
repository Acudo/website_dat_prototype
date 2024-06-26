import json
from datetime import date

data = {'streak': 0, 'lastlogin': '0000-00-00'}

def retrieve_data():
    file = open('data.json', 'r')
    data = json.load(file)
    if data['lastlogin'] != date.today():
        add_streak()
    return data

def add_streak():
    data['streak'] += 1

def save():     
    file = open('data.json', 'w')
    json.dump(data, file)

data = retrieve_data()
save()
print(data['streak'])
input()

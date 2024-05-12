import json

data = {'username': '',
        'streak': 0}

def retrieve_data():
    file = open('data.json', 'r')
    data = json.load(file)
    return data

def add_streak():
    data['streak'] += 1

def save():
    file = open('data.json', 'w')
    json.dump(data, file)

username = input("Username: ")
data = retrieve_data()
print(data['streak'])

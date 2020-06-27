import os

from pymongo import MongoClient as mc
myclient = mc("mongodb://localhost:27017/")
db = myclient["faceszakh"]
col = db["faces"]

cursor = col.find()
len = col.find().count()

dirname = os.path.dirname(__file__) + '/known_people'

times = {}
for i in range(len):
    times[cursor[i]['name'].replace(dirname, '')[1:-4]] = cursor[i]['time']

# print(times)
with open('jrnl.txt', 'w') as inp:
    print('Журнал посещений!', file = inp)
    for i in times:
        print('\n','User name: '+ i, file=inp)
        print('First added: ' + times[i][0], file=inp)
        a = [j for j in times[i][1:]]
        print('logs:', file=inp)
        for k in a:
            print(k, file=inp)

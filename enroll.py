import face_recognition
import os
import string
import random
from bson.binary import Binary
import pickle
from datetime import datetime

from pymongo import MongoClient as mc
myclient = mc("mongodb://localhost:27017/")
db = myclient["faceszakh"]
col = db["faces"]


def keygen(Length=16):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(Length))

#make array of sample pictures with encodings
known_face_encodings = []
known_face_names = []
dirname = os.path.dirname(__file__)
path = dirname+'/known_people/'

#make an array of all the saved jpg files' paths
names = [(path + f) for f in os.listdir(path)]

i = 0
while i < 2:
    try:
        globals()['image_{}'.format(i)] = face_recognition.load_image_file(names[i])
        globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
        encoding = (globals()['image_encoding_{}'.format(i)])
        uid = keygen(16)
        name = names[i]
        time = datetime.now()
        db.faces.insert_one({"uid": f"""{uid}""", "name": f"""{name}""", "time": [f"""{str(time)[:-7]}"""], "photo": Binary(pickle.dumps(encoding))})
        i += 1
        if i == 2:
            i = 0
            names = names[2:]
    except:
        break

print('photos enrolled')
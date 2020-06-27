from pymongo import MongoClient as mc
import numpy as np
from bson.binary import Binary
import pickle

myclient = mc("mongodb://localhost:27017/")

db = myclient["faceszakh"]

col = db["faces"]

db.faces.insert_one({"name": "Deleteme"})
#
# encoding = np.array([-1.26621529e-01,  1.14019729e-01,  6.44965842e-03, -2.50842124e-02,
#  -8.94455984e-02,  3.06660160e-02, 6.64121807e-02, -7.34225437e-02,
#   1.87906250e-01, -3.06377262e-02,  2.96320558e-01, -1.11832045e-01,
#  -2.51245856e-01, -2.47780196e-02, -3.23810168e-02,  1.46996662e-01,])

# dict = {"name": "Important experiment", "data": Binary(pickle.dumps(encoding))}
# col.insert_one(dict)

# x = col.find()
# print(x[6])
# a = [pickle.loads(x[6]['data'])]
# print(a)

col.delete_one({'name': {'$eq': 'Deleteme'}})

print('db created')
print(myclient.list_database_names())
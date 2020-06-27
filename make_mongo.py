from pymongo import MongoClient as mc
import numpy as np
from bson.binary import Binary
import pickle

myclient = mc("mongodb://localhost:27017/")

db = myclient["faceszakh"]

col = db["faces"]

db.faces.insert_one({"name": "Deleteme"})

col.delete_one({'name': {'$eq': 'Deleteme'}})

print('db created')
print(myclient.list_database_names())
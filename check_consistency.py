from pymongo import MongoClient
import datetime
import json

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client['MobilityDataLake_2']
collection = input_db['torino']

start = datetime.datetime(2016, 12, 1)
end = datetime.datetime.now()

cursor = collection.find({"timestamp":{'$gte': start, '$lt': end}})

count = 0
for document in cursor:

    if document["provider"] == "enjoy":
        car = document["state"][0]
        if car["lon"] < 8:
            count += 1

print count
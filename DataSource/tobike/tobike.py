import pybikes
from pymongo import MongoClient
import json
import time
import datetime


MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'MobilityDataLake'
client = MongoClient(MONGO_HOME)
db = client[DB_NAME]

def DBinsert (city, state):

    collection = db[city]
    record = {\
         "timestamp": datetime.datetime.now(),\
         "provider": "[TO]Bike",\
         "state": state\
         }
     
    try:
        collection.insert_one(record)
    except:
        print "Invalid data coding!"

toBike = pybikes.get('to-bike')
toBike.update()
state = ""
#for i in range(len(toBike.stations)):
l={}
stations_dict={}

for j in range(1):
    print "ok"
    for i in range(len(toBike.stations)):
        l["name"] = toBike.stations[i].name
        l["extra"] = toBike.stations[i].extra
        l["timestamp"] = str(toBike.stations[i].timestamp)
        l["free"] = toBike.stations[i].free
        l["bikes"] = toBike.stations[i].bikes
        l["longitude"] = toBike.stations[i].longitude
        l["latitude"] = toBike.stations[i].latitude
        stations_dict[i] = l
        l={}
    state = json.dumps(stations_dict)
    DBinsert("torino", state)
    time.sleep(60)






#any difference between not-in-service station and the empity station


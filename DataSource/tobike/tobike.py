import requests
from pymongo import MongoClient

import datetime
import time

import re
import json


MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'CSMS'

client = MongoClient(MONGO_HOME)
db = client.CSMS
db.authenticate('csms', '1234')

client = MongoClient(MONGO_HOME)
db = client[DB_NAME]

def DBinsert(provider,city, current_state):
    collection = db[city]
    record = {\
         "timestamp": datetime.datetime.now(),\
         "provider": provider,\
         "city" : city, \
         "state": current_state\
         }
     
#    return record
    try:
        collection.insert_one(record)
    except:
        print "Invalid data coding!"
        
class TObike():
    
    def __init__(self,provider,city):
        self.provider = provider
        self.city = city
        self.last_state = None
    
    #class counting the bikes' status for station 
    def tobike_bikes(self,bikes):
        assert len(bikes) == 30
    
        empty_places = bikes.count('0')
        available_bikes =  bikes.count('4')
        broken_bikes = bikes.count('1') + bikes.count('5')
        filler = bikes.count('x')
    
        assert empty_places + available_bikes + broken_bikes + filler == 30
    
        return {
            'empty_places': empty_places,
            'available_bikes': available_bikes,
            'broken_bikes': broken_bikes,
        }
    
    def get_data(self):
        r = requests.get("http://www.tobike.it/frmLeStazioni.aspx")
        r.raise_for_status()
        
        #REGEX expression to scrape the data
        RE = r"{RefreshMap\((?P<data>.*)\)}"
        result = re.search(RE, r.text, re.UNICODE).group("data")
        
        row = result.split("','")
    
        ids = row[0].split("|")
        num_votes = row[1].split("|")
        votes = row[2].split("|")
        lats = row[3].split("|")
        lngs = row[4].split("|")
        names = row[5].split("|")
        bikes = row[6].split("|")
        addresses = row[7].split("|")
        statuses = row[8].split("|")
    
        num_points = len(ids)
        assert num_points == len(num_votes)
        assert num_points == len(votes)
        assert num_points == len(lats)
        assert num_points == len(lngs)
        assert num_points == len(names)
        assert num_points == len(bikes)
        assert num_points == len(addresses)
        assert num_points == len(statuses)
    
        string = ids[0].split("'")
        ids[0] = string[1]
        l=[]
        d={}
        #print "++++"+ids[0]
        for i in range (num_points) :
            #print ids[i]
            d={
            'id': str(ids[i]),
            'onMapID': i,
            'num_votes': num_votes[i],
            'vote': votes[i],
            'lat': lats[i],
            'lng': lngs[i],
            'name': names[i],
            'bikes': self.tobike_bikes(bikes[i]),
            'address': addresses[i],
            'status': statuses[i]
            }
            l.insert(i,d)
            d={}
    
        return json.dumps(l)
        
if __name__ == "__main__":
    TB = TObike("tobike","torino")
    while(True) :
        DBinsert(TB.city,TB.provider,TB.get_data())
	time.sleep(60)
    


    
    

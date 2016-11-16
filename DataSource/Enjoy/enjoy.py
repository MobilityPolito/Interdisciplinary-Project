import threading

import requests
from pymongo import MongoClient

import json

import datetime
#import time

MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'MobilityDataLake'
client = MongoClient(MONGO_HOME)
db = client[DB_NAME]

API_KNOCK_URL_FORMAT = 'https://enjoy.eni.com/it/{city}/map/'
URL_HOME = 'https://enjoy.eni.com'
URL_COOKIE = 'https://enjoy.eni.com/ajax/set_cookie_pref_city'
URL_CARS =  'https://enjoy.eni.com/ajax/retrieve_vehicles'

cities = [{'city': 'torino'},\
           {'city': 'milano'},\
           {'city': 'catania'},\
           {'city': 'roma'},\
           {'city': 'firenze'}]

sessions = {city['city']: None for city in cities}
check_sessions = {city['city']: False for city in cities}         

def DBinsert (city, state):

    collection = db[city]
    record = {\
         "timestamp": datetime.datetime.now(),\
         "provider": "enjoy",\
         "state": state\
         }
     
    try:
        collection.insert_one(record)
    except:
        print "Invalid data coding!"
        
class CityThread (threading.Thread):
    
    def __init__(self, city):

        threading.Thread.__init__(self)
        self.stopped = False
        self.city = city
        
    def run(self):
        
        print threading.current_thread()
    
        try:
            URL_HOME = 'https://enjoy.eni.com/it/' + self.city['city'] + '/map/'
            session = requests.Session()
            session.get(URL_HOME)
            session.post(URL_COOKIE, data=json.dumps(self.city))
        except:
            print "Session error!"
            
        for i in range (1):
        		
            try:
                request = session.get(URL_CARS)
            except:
                print "HTTP error!"
                
            state = json.loads(request.text)
            
            DBinsert(self.city['city'], state)
            with open (self.city['city'] + ".json", "w+") as outfile:
                outfile.write(json.dumps(state))
                
if __name__ == "__main__":
    
    for city in cities:
        print city
        thread = CityThread(city)
        thread.start()

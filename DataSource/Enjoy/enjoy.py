import threading

import requests
from pymongo import MongoClient

import json

import datetime
import time

MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'MobilityDataLake'

URL_HOME = 'https://enjoy.eni.com'
URL_AJAX = URL_HOME + '/ajax/'
#URL_COOKIE = URL_AJAX + 'set_cookie_pref_city'
URL_CARS =  URL_AJAX + 'retrieve_vehicles'

client = MongoClient(MONGO_HOME)
db = client[DB_NAME]

def write_log (message):
    with open("enjoy.log", "a+") as f:
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        f.write("[" + timestamp + "] -> " + message + "\n")

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
        self.last_state = None
        
    def run(self):
        
        print threading.current_thread()
    
        try:
            URL_HOME = 'https://enjoy.eni.com/it/' + self.city + '/map/'
            session = requests.Session()
            session.get(URL_HOME)
            #session.post(URL_COOKIE, data=json.dumps(self.city))
            write_log(self.city + ": session successfully started")            
        except:
            print "Session error!"
            
        while(True):
        
            try:
                request = session.get(URL_CARS)
                state = json.loads(request.text)
                self.last_state = state
                write_log(self.city + ": state successfully loaded")
            except:
                write_log(self.city + ": HTTP error!")
                
            try:
                DBinsert(self.city, state)
                write_log(self.city + ": state successfully inserted")                
            except:
                write_log(self.city + ": Database error!")

            try:
                with open (self.city + "_last_state.json", "w+") as outfile:
                    outfile.write(json.dumps(state))
                write_log(self.city + ": state successfully written")                    
            except:
                write_log(self.city + ": File write error!")
                
            time.sleep(300)
                
if __name__ == "__main__":
        
    cities = ['torino',\
               'milano',\
               'catania',\
               'roma',\
               'firenze']
    
    for city in cities:
        print city
        thread = CityThread(city)
        thread.start()
    thread.join()

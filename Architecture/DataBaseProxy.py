import datetime

from pymongo import MongoClient

import pandas as pd

client = MongoClient('mongodb://localhost:27017/')

class DataBaseProxy (object):
    
    def __init__ (self):
        
        self.db_raw = client['CSMS']
        self.db_fix_providers = client['CSMS_']
        self.db_fix_cities = client['CSMS__']
        self.db_compressed = client['CSMS___']

    def insert (self, provider, city, state):
    
        record = {
                     "timestamp": datetime.datetime.now(),
                     "provider": provider,
                     "state": state
                 }

        collection = self.db_raw[city]            
        try:
            collection.insert_one(record)
        except:
            print "Invalid data coding!"
            
    def query (self, provider, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            start, end = args
            return self.db_compressed[city].find \
                    ({"timestamp":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":"enjoy"
                    }).sort([("timestamp", 1)])
                

    def fix_providers(self):
        
        input_db = self.db_raw
        output_db = self.db_fix_providers
        
        for city in ['torino','milano']:
    
            input_collection = input_db[city]
            output_collection = output_db[city]
            
            cursor = input_collection.find()
            
            for document in cursor:
                
                if type(document["state"]) == dict:
                    document["provider"] = "car2go"
                
                elif type(document["state"]) == list:
                    document["provider"] = "enjoy"
                
                elif type(document["state"]) == unicode:
                    document["provider"] = "tobike"
                    
                output_collection.insert_one(document)
    
            
    def fix_cities (self):
        
        input_db = self.db_fix_providers
        output_db = self.db_fix_cities
    
        torino_collection = output_db['torino']        
        milano_collection = output_db['milano']
        
        def check_cap (cap):
            if cap.startswith("10"):
                torino_collection.insert_one(document)
            elif cap.startswith("20") or cap == "Milano" or cap == "Segrate":
                milano_collection.insert_one(document)
            else:
                print "Unknown CAP: " + cap
        
        for city in ['torino','milano']:
    
            input_collection = input_db[city]
            cursor = input_collection.find()
            
            for document in cursor:
                if document["provider"] == "enjoy":
                    car = document["state"][0]
                    
                    if len(car["address"].split(',')) == 3:
                        cap = car["address"].split(',')[2].split(' ')[1]
                    elif len(car["address"].split(',')) == 2:
                        cap = car["address"].split(',')[1].split(' ')[1]
                    else:
                        cap = ""
                    check_cap(cap)
                else:
                    torino_collection.insert_one(document)
                            
    def compress (self):
    
        input_db = self.db_fix_cities
        output_db = self.db_compressed
        
        for city in ["milano","torino"]:
            for provider in ["enjoy","car2go","tobike"]:
        
                input_collection = input_db[city]
                output_collection = output_db[city]
                
                cursor = input_collection.find({"provider":provider})
                
                last = cursor.next()
                output_collection.insert_one(last)
                
                for document in cursor:
                    current = document
                    try:
                        last_df = pd.DataFrame(last["state"])
                        current_df = pd.DataFrame(current["state"])
                        if not last_df.equals(current_df):
                            output_collection.insert_one(document)
                    except:
                        print type(current["state"])
                    last = document

dbp = DataBaseProxy()
#dbp.fix_providers()
#dbp.fix_cities()
dbp.compress()

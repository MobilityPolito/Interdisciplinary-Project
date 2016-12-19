import datetime

import pandas as pd

from Provider import Provider

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
            
class Enjoy(Provider):
    
    def __init__ (self):
        self.name = "enjoy"
    
    def select_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            start, end = args
            self.cursor = dbp.query_time(self.name, city, start, end)

        return self.cursor
        
    def get_fields(self):
        
        self.cursor.rewind()
        sample_columns = pd.DataFrame(self.cursor.next()["state"]).columns
        for doc in self.cursor:
            columns = pd.DataFrame(doc["state"]).columns
            if len(columns.difference(sample_columns)):
                print "Warning: different fields for the same provider"
            
        self.fields = columns
        return self.fields
        
    def get_fleet(self):

        self.cursor.rewind()        
        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                 .loc[:, "car_plate"].values)
        self.fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                     .loc[:, "car_plate"].values)
            self.fleet = self.fleet.union(current_fleet)
        return self.fleet

def test():
    
    enjoy = Enjoy()
    
    end = datetime.datetime(2016, 11, 20, 13, 0, 0)
    start = end - datetime.timedelta(hours = 1)
    
    enjoy.select_data("torino","timestamp", start, end)    
    enjoy.get_fields()
    enjoy.get_fleet()
    
    return enjoy
    
enjoy = test()
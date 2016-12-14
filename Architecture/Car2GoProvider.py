#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:43:59 2016

@author: Flavia
"""

import datetime
import pandas as pd

from Provider import Provider
from DataBaseProxy import dbp

stop_car2go = False

class Car2Go(Provider):
    
    def __init__ (self):
        self.name = "car2go"
    
    def get_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.cursor = dbp.query(self.name, city, by, args[0], args[1])

    def get_fields(self):
        
        doc = self.cursor.next()
        return pd.DataFrame(doc["state"]["placemarks"])
        
    def get_fleet(self):
        
        self.fleet = pd.Index()
        
    def track_car(self, plate):
        
        self.cursor.rewind()
        for doc in self.cursor:
            df = pd.DataFrame(doc["state"]["placemarks"])
            car = df[df["name"] == plate]
            if len(car):
                pass
            else:
                print doc["timestamp"]
                print "in use"
        
car2go = Car2Go()
end = datetime.datetime(2016, 11, 22, 18, 0, 0)
start = end - datetime.timedelta(hours = 6)
#print start, end
car2go.get_data("torino","timestamp", start, end)
df = car2go.get_fields()
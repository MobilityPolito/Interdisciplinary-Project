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
        self.name = "enjoy"
    
    def get_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.cursor = dbp.query(self.name, city, by, args[0], args[1])

    def get_fields(self):
        
        sample_columns = pd.DataFrame(self.cursor.next()["state"]).columns
        for doc in self.cursor:
            columns = pd.DataFrame(doc["state"]).columns
            if len(columns.difference(sample_columns)):
                print "Warning: different fields for the same provider"
            
        self.fields = columns
        
    def get_fleet(self):
        
        self.fleet = pd.Index()
        
car2go = Car2Go()
end = datetime.datetime(2016, 12, 1, 1, 0, 0)
start = end - datetime.timedelta(hours = 1)
car2go.get_data("torino","timestamp", start, end)
car2go.get_fields()
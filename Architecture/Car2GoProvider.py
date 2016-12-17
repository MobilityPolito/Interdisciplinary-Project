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
        self.city = "torino"
    
    def get_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.cursor = dbp.query(self.name, city, by, args[0], args[1])

    def get_fields(self):
        
        doc = self.cursor.next()
        return list(pd.DataFrame(doc["state"]["placemarks"]).columns)

    def get_fleet(self):

        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                 .loc[:,"name"].values)
        fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                     .loc[:,"name"].values)
            fleet = fleet.union(current_fleet)
        return list(fleet)

    def track_car(self, car_plate):

        def get_car_status (doc):
            df = pd.DataFrame(doc["state"]["placemarks"])
            car = df[df["name"] == car_plate]
            if len(car):
                return "parked"
            else:
                return "booked"
        
        self.cursor.rewind()
        doc = self.cursor.next()
        
        last_car_status = get_car_status(doc)
        start = doc["timestamp"]
        try:
            df = pd.DataFrame(doc["state"]["placemarks"])
            lat = list(df[df["name"] == car_plate]["coordinates"].values)[0][1]
            lon = list(df[df["name"] == car_plate]["coordinates"].values)[0][0]
        except:
            print doc["_id"], car_plate
            
        for doc in self.cursor:
            try:
                current_car_status = get_car_status(doc)
                if last_car_status == "parked":
                    if last_car_status == current_car_status:
                        pass
                    else:
                        end = doc["timestamp"]
                        dbp.insert_park(self.name, self.city, car_plate, lat, lon, start, end)
                        last_car_status = current_car_status
                elif current_car_status == last_car_status == "booked":
                    start = doc["timestamp"]
                elif current_car_status == "parked" and last_car_status == "booked":
                    last_car_status = current_car_status
                    df = pd.DataFrame(doc["state"]["placemarks"])
                    lat = list(df[df["name"] == car_plate]["coordinates"].values)[0][1]
                    lon = list(df[df["name"] == car_plate]["coordinates"].values)[0][0]
            except:
                print doc["_id"]

car2go = Car2Go()

end = datetime.datetime(2016, 11, 25, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

car2go.get_data("torino","timestamp", start, end)

fields = car2go.get_fields()
fleet = car2go.get_fleet()
for car in fleet:
    car2go.track_car(car)
    

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:43:59 2016

@author: Flavia
"""

import datetime
import pandas as pd

from Provider import Provider

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

class Car2Go(Provider):
    
    def __init__ (self):
        self.name = "car2go"
        self.city = "torino"
    
    def select_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            start, end = args
            self.cursor = dbp.query_time(self.name, city, start, end)

    def get_fields(self):
        
        doc = self.cursor.next()
        return list(pd.DataFrame(doc["state"]["placemarks"]).columns)

    def get_fleet(self):

        self.cursor.rewind()        
        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                 .loc[:,"name"].values)
        self.fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                     .loc[:,"name"].values)
            self.fleet = self.fleet.union(current_fleet)
        return self.fleet

    def get_parks(self, car_plate):

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
        
        if last_car_status == "parked":
            try:
                start = doc["timestamp"]
                df = pd.DataFrame(doc["state"]["placemarks"])
                car_state = df[df["name"] == car_plate]
                lat = list(car_state["coordinates"].values)[0][1]
                lon = list(car_state["coordinates"].values)[0][0]
            except:
                print df.describe()

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

def test():
    
    car2go = Car2Go()
    
    end = datetime.datetime(2016, 11, 25, 0, 0, 0)
    start = end - datetime.timedelta(days = 1)
    
    car2go.select_data("torino","timestamp", start, end)    
    car2go.get_fields()
    car2go.get_fleet()
    
    for car in list(car2go.fleet):
        car2go.get_parks(car)
        
    return car2go
    
car2go = test()
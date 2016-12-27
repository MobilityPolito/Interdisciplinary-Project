#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:26:00 2016

@author: root
"""
from DataBaseProxy import DataBaseProxy

import googlemaps
from datetime import timedelta
import datetime

import pandas as pd

dbp = DataBaseProxy()
gmaps = googlemaps.Client(key='AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY')

# Books durations

def get_books (provider, city, start, end):

    books_cursor = dbp.query_book_by_time(provider, city, start, end)
    
    books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
    for doc in books_cursor:
        s = pd.Series(doc)
        books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    

    return books_df
    
#def get_directions():
#    
#    directions_result = gmaps.directions("via giovanni fattori 4, Torino",
#                                     "porta nuova,Torino",
#                                     mode="transit",
#                                     departure_time=an_hour_from_now)
    
    
end = datetime.datetime(2016, 11, 25, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

books_df = get_books("car2go","torino", start, end)    

for index, row in books_df.iterrows():
    origin = gmaps.reverse_geocode((row['start_lat'],  row['start_lon']))
    destination = gmaps.reverse_geocode((row['end_lat'], row['end_lon']))
    directions_result = gmaps.directions(origin,
                                    destination,
                                     mode="transit",
                                     departure_time=row['start'])
#
#    
#
#
## Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
## Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit


    
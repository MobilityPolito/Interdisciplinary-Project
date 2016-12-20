#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:26:00 2016

@author: root
"""

import googlemaps
import pprint
from datetime import timedelta
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
an_hour_from_now = datetime.now() + timedelta(hours=1)
directions_result = gmaps.directions("via giovanni fattori 4, Torino",
                                     "porta nuova,Torino",
                                     mode="transit",
                                     departure_time=an_hour_from_now)

pp = pprint.PrettyPrinter(indent=4)

    
import threading
import logging
import requests
import datetime
import time
import json

import pandas as pd

from DataSource import RTDS
from Provider import Provider
from DataBaseProxy import dbp

stop_enjoy = False

class EnjoyRTDS(RTDS):
    
    def __init__ (self, city):

        threading.Thread.__init__(self)        
        self.name = "enjoy"
        self.log_filename = "rtds.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)        
        
        self.city = city
        self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
        self.url_data = 'https://enjoy.eni.com/ajax/retrieve_vehicles'

    def log_message (self, scope, status):
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)        
        
    def start_session (self):
        
        try:
            self.session = requests.Session()
            self.session.get(self.url_home)
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        logging.debug(message)
            
    def get_feed (self):
        
        if (datetime.datetime.now() - self.session_start_time).total_seconds() > 2400:
            self.session = self.session.close()
            self.start_session()
            self.session_start_time = datetime.datetime.now()

        try:
            feed = json.loads(self.session.get(self.url_data).text)
            message = self.log_message("feed","success")
        except:
            feed = {}
            message = self.log_message("feed","error")
        logging.debug(message)

        return feed
        
    def check_feed (self, feed):
        
        last_feed_df = pd.DataFrame(self.last_feed)
        current_feed_df = pd.DataFrame(self.current_feed)
        print last_feed_df.equals(current_feed_df)
        
        print current_feed_df.index
        print current_feed_df.columns
        
        for col in current_feed_df.columns:
            s = current_feed_df[col]
            print str(s.dtype)
#            if str(s.dtype) != "object":
#                print s.describe()

    def to_DB (self):
    
        dbp.insert(self.name, self.city, self.current_feed)
        
    def run(self):
        
        print threading.current_thread()
    
        self.start_session()
        
        self.last_feed = self.get_feed()
        
        while stop_enjoy is False:
            self.current_feed = self.get_feed()
            self.check_feed()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(10)
        else:
            return

#enjoy_rtds = EnjoyRTDS("torino")
#enjoy_rtds.start()            
            
class Enjoy(Provider):
    
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
        
enjoy = Enjoy()
end = datetime.datetime(2016, 12, 1, 1, 0, 0)
start = end - datetime.timedelta(hours = 1)
enjoy.get_data("milano","timestamp", start, end)
enjoy.get_fields()
from pymongo import MongoClient
import datetime
import json
from bson import json_util
import logging

LOG_FILENAME = 'rental.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client.test
#input_db.authenticate('csms', '1234')
collection = input_db['torino']
collection_cars = input_db['enjoy_fleet']

# cursor = collection.find({'provider':'enjoy'}).limit(1)
cursor = collection.find({'provider':'enjoy'}).sort('_id')
cursor_cars = collection_cars.find()

cars = 	{ 'EZ500DD': 	{	'plate':'EZ500DD',
							'rent':0,
							'last_lon':0,
							'last_presence':0 
						} 
		}

# for doc in cursor_cars:
# 	cars[doc['plate']] = {}


for doc in cursor:

	found = 1
	for available_car in doc['state']:

		if cars['EZ500DD']['plate'] in available_car['car_plate']:
			
			if cars['EZ500DD']['rent'] == 1:

				print 'moved from {} to {}'.format(cars['EZ500DD']['last_lon'], available_car['lon'])
				print 'init {} finish {}'.format(cars['EZ500DD']['last_presence'], doc['timestamp'])

				cars['EZ500DD'].update({
										'last_lon': available_car['lon'],
										'last_lat': available_car['lat'],
										'last_presence': doc['timestamp'],
										'rent': 0
									})

			else:
				cars['EZ500DD'].update({
									'last_lon': available_car['lon'],
									'last_lat': available_car['lat'],
									'last_presence': doc['timestamp'],
									'rent': 0
									})
		else:
			if cars['EZ500DD']['rent'] == 0 and found == 1:
				cars['EZ500DD'].update({'rent': 1})
				found = 0
				print 'qui dentro!!!-----------------'
			else:
				pass


	# try:
	# 	for available_car in doc['state']:
	# 		if available_car['car_plate'] not in cars:
	# 			cars.append(available_car['car_plate'])
	# except:
	# 	count_error += 1
	# 	message = 'ERROR! in entry {}'.format(doc['_id'])
	# 	logging.debug(message)

# print cars
# print cars['EZ500DD']['last_pos']
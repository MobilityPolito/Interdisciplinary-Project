import requests
import json
#import cookielib

URL_HOME = 'https://enjoy.eni.com'
URL_COOKIE = 'https://enjoy.eni.com/ajax/set_cookie_pref_city'
URL_CARS =  'https://enjoy.eni.com/ajax/retrieve_vehicles'

session = requests.Session()
data_city = {'city': 'torino'}

session.get(URL_HOME)
session.post(URL_COOKIE, data=json.dumps(data_city))
r=session.get(URL_CARS)


#print(r.text)
with open('prova.txt','w+') as outputfile:
	outputfile.write(r.text) 
import requests
import json
import time

URL_HOME = 'https://enjoy.eni.com'
URL_COOKIE = 'https://enjoy.eni.com/ajax/set_cookie_pref_city'
URL_CARS =  'https://enjoy.eni.com/ajax/retrieve_vehicles'

data_city = {'city': 'torino'}

def main():

	checkSession = False;
	while (1):

		#check if session is still valid (not implemented yet)
		if not checkSession: 
			session = requests.Session()
			session.get(URL_HOME)
			session.post(URL_COOKIE, data=json.dumps(data_city))
			checkSession = True
		
		request = session.get(URL_CARS)

		#Write response on file for now
		#Later the response will be pushed into Mongodb
		with open('prova.txt','a') as outputfile:
			outputfile.write(request.text)

		time.sleep(60) 

if __name__ == '__main__':
	main()
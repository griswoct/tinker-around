'''
#WEATHER LOOKUP
#PURPOSE: LOOK UP WEATHER CONDITIONS VIA PYTHON SCRIPT
#LICENSE: THE UNLICENSE
#AUTHOR: CALEB GRISWOLD
#CREATED: 09/24/2025
'''
#Use NOAA api: https://api.weather.gov/
#Need to figure out how to get location and pass to API
import requests

api_url = "https://api.weather.gov/"
coordinates = input("Where are you located? (latitude,longitude): ")
print("Coordinates: ",coordinates)  #for testing
location = requests.get("https://api.weather.gov/points/"+coordinates)
print("Location: ",location)
type = "/stations/" + location + "/observations/latest"
url = api_url+location

response = requests.get(url+type)

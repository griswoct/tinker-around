'''
#WEATHER LOOKUP
PURPOSE: LOOK UP WEATHER CONDITIONS VIA PYTHON SCRIPT
LICENSE: THE UNLICENSE
AUTHOR: CALEB GRISWOLD
CREATED: 09/24/2025
'''
#Use NOAA api: https://api.weather.gov/
#Need to figure out how to get location and pass to API
import requests

base_url = "https://api.weather.gov/"
location = ""  #Station ID goes here
type = "/stations/" + location + "/observations/latest"

response = requests.get(url)

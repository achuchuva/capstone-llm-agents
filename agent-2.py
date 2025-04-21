print("hello world")
import json
from pydantic import BaseModel
from autogen import ConversableAgent
from autogen.tools.dependency_injection import BaseContext
import requests



import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta, timezone


def weather_calculation(lat, lon, date, time):#requires very spercific formatting :(. code from https://open-meteo.com/en/docs?latitude=-38.0702&longitude=145.4741&timezone=auto
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "wind_speed_10m"],
        "timezone": "auto",
        #"forecast_days": 2#can change to get a larger forcast range or a date range. NOTE: i think using this is the best over date
        "start_date": date,#seems to strugle getting the correct date
	    "end_date": date
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {#https://github.com/open-meteo/open-meteo/issues/850 fix for timezone issue
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True).tz_convert(
                timezone(timedelta(seconds=response.UtcOffsetSeconds()))
            ),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True).tz_convert(
                timezone(timedelta(seconds=response.UtcOffsetSeconds()))
            ),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["precipitation"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    #print(hourly_dataframe)
    i = 0
    for val in hourly_dataframe["date"]:
        print(val)
        if date in str(val):#needs to be a string to compare
            if time in str(val):
                print("^ This is the date ^")
                tempreture = str(hourly_dataframe["temperature_2m"][i]) + "°C"
                rain_chance = str(hourly_dataframe["precipitation_probability"][i])+ "%"
                precipitation_amount = str(hourly_dataframe["precipitation"][i])+ " mm" #i think precipitation is mostly rain but could include snow if cold which is why i picked it over rain
                wind_speed = str(hourly_dataframe["wind_speed_10m"][i]) + " km/h"
        i = (i + 1)

    print("\nThe weather results for laditude " + str(latitude) + ", longditude " + str(longitude) + " at " + time + " on the " + date + " is:\n")
    print("Tempreture " + tempreture)
    print("Rain chance " + rain_chance)
    print("Precipitation amount " + precipitation_amount)
    print("Wind speed " + wind_speed)
    return hourly_dataframe


###Curent input field###
latitude = -38.0702 #51.5085#-38.0702 works for other time zones so far the tests were pakenham and london
longitude = 145.4741 #-0.1257#145.4741
date = "2025-04-21"
time = "12:00"#note midnight has to be represented with 00:00
weather_results = weather_calculation(latitude, longitude, date, time)

#print(weather_results)#good for testing results
#print(weather_results["date"])
#print(weather_results["date"][1])







class Location(BaseModel):
    name: str
    # future implementation could be lat/long

class WeatherRequest(BaseContext, BaseModel):
    location: str
    date: str
    time: str

class WeatherResponse(BaseContext, BaseModel):
    location: str
    laditude: str
    longditude: str
    date: str
    time: str
    tempreture: str
    rain_chance: str
    precipitation_amount: str
    wind_speed: str

llm_config = {
    "model": "gemma3:4b",
    "api_type": "ollama",
    "temperature": 0.5,
}

weather_request_agent = ConversableAgent(  # declaring agent
    name="request_agent",
    system_message="""
    Extract requested details from the user and return ONLY this JSON format:
    {
        "location": {"name": "requested_location"},
        "date": {"name": "requested_date"},
        "time": "requested_time"
    }
    Return NOTHING else - no text or explanations just the raw JSON.""",    # system prompt to tailor output
    llm_config=llm_config,
)

weather_response_agent = ConversableAgent(
    name="response_agent",
    system_message="""
    Given the requested details, generate the latitude and longditude of the given location and from here predict the tempreture, rain chance, precipitation amount and wind speed based off the date, time, latitude and longditude.
    Format the response as:
    {
        "location": {"name": "requested_location"},
        "laditude": {"name": "laditude_created"},
        "longditude": "longditude_created",
        "date": {"name": "requested_date"},
        "time": {"name": "requested_time"},
        "tempreture": "predicted_tempreture",
        "rain_chance": {"name": "predictedrain_chance"},
        "precipitation_amount": {"name": "predicted_precipitation_amount"},
        "wind_speed": "predicted_wind_speed",
    }
    The location, date and time should be provided based off the request agent. The latitude and longditude you must come up with yourself. The tempreture, rain chance, precipitation amount and wind speed you can make up the best you can.
    Return NOTHING else - no text or explanations just the raw JSON.""",
    llm_config=llm_config,
)

coordinator = ConversableAgent(
    name="coordinator_agent",
    system_message="Coordinate between request and response agents to generate the weather prediction for the given location.",
    llm_config=llm_config,  # 'inbetween' agent
)

user_message = "I want to know the weather in Pakenham at 12:00 on the 21-04-2025"
'''
#user_messages = {
#
#}   add more stuff
'''

chat_results = coordinator.initiate_chats([
    {"recipient": weather_request_agent, "message": user_message, "max_turns": 1}
])

travel_details = None
if chat_results:
    travel_details = chat_results[0].summary

if travel_details:
    chat_results = coordinator.initiate_chats([
        {"recipient": weather_response_agent, "message": travel_details, "max_turns": 1}
    ])
    if chat_results:
        print(chat_results[0].summary)
else:
    print("\n\nNo travel details available.")





'''
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": -38.0702,
	"longitude": 145.4741,
	"hourly": ["temperature_2m", "precipitation_probability", "precipitation"],
	"timezone": "auto",
	"forecast_days": 2#can change to get a larger forcast range or a date range
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
'''



'''
url = "https://sws-data.sws.bom.gov.au/api/v1/get-k-index"
headers = {'Content-Type': 'application/json; charset=UTF-8'}
requestBody = {
  'api_key': '17db5a7d-ddd0-4b3a-95ac-80cf08ef58cc',
  'options': { 'location': 'Canberra'}}

response = requests.post(url, headers=headers, json=requestBody)

if response.status_code == 200:
  responseBody = response.json()
  data = responseBody['data']
  print(data)
else:
  responseBody = response.json()
  errors = responseBody['errors']
  print(errors)
'''





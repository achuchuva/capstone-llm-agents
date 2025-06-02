print("hello world")
from autogen import ConversableAgent


import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta, timezone

from autogen import GroupChat
from autogen import GroupChatManager
import autogen

def weather_calculation(
    lat: str, lon: str, date: str, time: str
):  # requires very spercific formatting :(. code from https://open-meteo.com/en/docs?latitude=-38.0702&longitude=145.4741&timezone=auto

    print("Using weather calculation function")
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": float(lat),
        "longitude": float(lon),
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
        ],
        "timezone": "auto",
        # "forecast_days": 2#can change to get a larger forcast range or a date range. NOTE: i think using this is the best over date
        "start_date": str(date),  # seems to strugle getting the correct date
        "end_date": str(date),
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

    hourly_data = (
        {  # https://github.com/open-meteo/open-meteo/issues/850 fix for timezone issue
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
    )

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["precipitation"] = hourly_precipitation

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    # print(hourly_dataframe)
    i = 0

    tempreture = "0°C"
    rain_chance = "0%"
    precipitation_amount = "0 mm"
    wind_speed = "0 km/h"

    for val in hourly_dataframe["date"]:
        print(val)
        if date in str(val):  # needs to be a string to compare
            if time in str(val):
                print("^ This is the date ^")
                tempreture = str(hourly_dataframe["temperature_2m"][i]) + "°C"
                rain_chance = (
                    str(hourly_dataframe["precipitation_probability"][i]) + "%"
                )
                precipitation_amount = (
                    str(hourly_dataframe["precipitation"][i]) + " mm"
                )  # i think precipitation is mostly rain but could include snow if cold which is why i picked it over rain
                wind_speed = str(hourly_dataframe["wind_speed_10m"][i]) + " km/h"
        i = i + 1

    return (
        "\nThe weather results for laditude "
        + str(lat)
        + ", longditude "
        + str(lon)
        + " at "
        + time
        + " on the "
        + date
        + " is:\n"
        + "Tempreture "
        + tempreture
        + "\nRain chance "
        + rain_chance
        + "\nPrecipitation amount "
        + precipitation_amount
        + "\nWind speed "
        + wind_speed
    )


from autogen import register_function


llm_config = {
    # "model": "gemma3:4b",
    "model": "llama3.2",  # for some reason gemma3 does not have the tools or something to use the functions
    "api_type": "ollama",
    "temperature": 0.5,
}

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   human_input_mode="ALWAYS",
   code_execution_config=False,
   description="A human user capable of working with Autonomous AI Agents.",
)

weather_agent = ConversableAgent(  # declaring agent
    name="request_agent",
    system_message="""
    Extract requested details from the user and return ONLY this JSON format:
    {
        "location": {"name": "requested_location"},
        "date": {"name": "requested_date"},
        "time": "requested_time"
    }
    Return NOTHING else - no text or explanations just the raw JSON.""",  # system prompt to tailor output
    llm_config=llm_config,
)


# https://microsoft.github.io/autogen/0.2/docs/tutorial/chat-termination/ example passing through messages
weather_agent = ConversableAgent(  # declaring agent
    name="weather_agent",
    system_message="""
    Given the provided details, generate the latitude and longditude of the location and then use the weather calculator to find the rest of the detais to fill in the format bellow. When you use the calculater make sure to format the date as (dd-mm-yyyy). the time should be formated as (xx:xx). latitude and longditude should be floats. make sure to first put in the latitude, then the longditude, then the date and then the time
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
    The location, date and time should be provided based off the location agent. The latitude and longditude you must use what is provided. The tempreture, rain chance, precipitation amount and wind speed you can make up the best you can.
    Return NOTHING else - no text or explanations just the raw JSON.""",  # system prompt to tailor output
    llm_config=llm_config,
)

location_agent = ConversableAgent(
    name="location_agent",
    system_message="""Your Job is to only create the latitude and longditude of the requested location and then provide them as well as the name of the location, date and time to the weather agent.
    Format the response as:
    {
        "location": {"name": "requested_location"},
        "laditude": {"name": "laditude_created"},
        "longditude": "longditude_created",
        "date": {"name": "requested_date"},
        "time": {"name": "requested_time"},
    }

    do not include any other messages
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

temp_travel_agent = ConversableAgent(
    name="travel_agent",
    system_message="""Your Job is to work out the time it takes to get from one location to another.
    Format the response as:
    {
        "start_location": {"name": "requested_location"},
        "end_location": {"name": "laditude_created"},
        "time_taken": "longditude_created",
    }

    do not include any other messages
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

# https://microsoft.github.io/autogen/0.2/docs/tutorial/tool-use/
# Register the calculator function to the two agents.
register_function(
    weather_calculation,
    caller=location_agent,  # The assistant agent can suggest calls to the calculator.
    executor=weather_agent,  # The user proxy agent can execute the calculator calls.
    name="weather_calculator",  # By default, the function name is used as the tool name.
    description="A function which uses latitude, longditude, date and time to calculate the weather",  # A description of the tool.
)

user_message = (
    "I want to know the weather in Pakenham victoria at 12:00 on the 21-04-2025"
)
user_message2 = (
    "I want to know how long it takes to get between pakenham and richmond station in victoria"
)

#user_message3 = input("Enter a query here -->")
#result = location_agent.initiate_chat(weather_agent, message=user_message, max_turns=3)


groupchat = GroupChat(agents=[weather_agent, location_agent, temp_travel_agent ], messages=[], max_round=6)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(manager, message=user_message)

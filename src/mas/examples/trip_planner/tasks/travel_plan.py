from datetime import datetime
import json

from pydantic import BaseModel
from autogen import ConversableAgent
from autogen.tools.dependency_injection import BaseContext


class Location(BaseModel):
    name: str


class TravelRequest(BaseModel):
    start: Location
    destination: Location
    time: str


class TravelResponse(BaseModel):
    start: Location
    destination: Location
    time_taken: str
    transport: str


def do_travel_plan():

    # just one line for the moment and going to city
    FAUX_DATA = {
        "Pakenham": {
            "stations": [
                {
                    "name": "East Pakenham Station",
                    "departure_times": ["08:04", "08:21", "08:31", "08:43"],
                },
                {
                    "name": "Pakenham Station",
                    "departure_times": ["08:07", "08:24", "08:34", "08:46"],
                },
                {
                    "name": "Cardinia Station",
                    "departure_times": ["08:11", "08:28", "08:38", "08:50"],
                },
                {
                    "name": "Officer Station",
                    "departure_times": ["08:14", "08:31", "08:41", "08:53"],
                },
                {
                    "name": "Beaconsfield Station",
                    "departure_times": ["08:18", "08:35", "08:45", "08:57"],
                },
                {
                    "name": "Berwick Station",
                    "departure_times": ["08:21", "08:38", "08:48", "09:00"],
                },
                {
                    "name": "Narre Warren Station",
                    "departure_times": ["08:24", "08:41", "08:51", "09:03"],
                },
                {
                    "name": "Hallam Station",
                    "departure_times": ["08:28", "08:45", "08:55", "09:07"],
                },
                {
                    "name": "Dandenong Station",
                    "departure_times": ["08:34", "08:51", "09:01", "09:13"],
                },
                {
                    "name": "Yarraman Station",
                    "departure_times": ["08:37", "08:54", "09:04", "09:16"],
                },
                {
                    "name": "Noble Park Station",
                    "departure_times": ["08:40", "08:57", "09:07", "09:19"],
                },
                {
                    "name": "Sandown Station",
                    "departure_times": ["08:42", "08:59", "09:09", "09:21"],
                },
                {
                    "name": "Springvale Station",
                    "departure_times": ["08:44", "09:01", "09:11", "09:23"],
                },
                {
                    "name": "Westall Station",
                    "departure_times": ["08:47", "09:04", "09:14", "09:26"],
                },
                {
                    "name": "Clayton Station",
                    "departure_times": ["08:49", "09:06", "09:16", "09:28"],
                },
                {
                    "name": "Huntingdale Station",
                    "departure_times": ["08:52", "09:09", "09:19", "09:31"],
                },
                {
                    "name": "Oakleigh Station",
                    "departure_times": ["08:55", "09:12", "09:22", "09:34"],
                },
                {
                    "name": "Hughesdale Station",
                    "departure_times": ["08:57", "09:14", "09:24", "09:36"],
                },
                {
                    "name": "Murrumbeena Station",
                    "departure_times": ["08:59", "09:16", "09:26", "09:38"],
                },
                {
                    "name": "Carnegie Station",
                    "departure_times": ["09:01", "09:18", "09:28", "09:40"],
                },
                {
                    "name": "Caulfield Station",
                    "departure_times": ["09:04", "09:22", "09:31", "09:43"],
                },
                {
                    "name": "South Yarra Station",
                    "departure_times": ["09:12", "09:30", "09:40", "09:51"],
                },
                {
                    "name": "Richmond Station",
                    "departure_times": ["09:15", "09:33", "09:43", "09:54"],
                },
            ]
        }
    }

    def faux_travel_lookup(travel: TravelRequest) -> TravelResponse:
        stations = FAUX_DATA.get("Pakenham", {}).get("stations", [])
        start_station = next(
            (s for s in stations if travel.start.name.lower() in s["name"].lower()),
            None,
        )
        dest_station = next(
            (
                s
                for s in stations
                if travel.destination.name.lower() in s["name"].lower()
            ),
            None,
        )

        if not start_station or not dest_station:
            return TravelResponse(
                start=travel.start,
                destination=travel.destination,
                time_taken="unknown",
                transport="no valid train found",
            )

        try:
            arrival_deadline = datetime.strptime(travel.time.strip().lower(), "%I:%M%p")
        except ValueError:
            return TravelResponse(
                start=travel.start,
                destination=travel.destination,
                time_taken="unknown",
                transport="invalid time format",
            )

        departure_times = [
            datetime.strptime(t, "%H:%M") for t in start_station["departure_times"]
        ]
        arrival_times = [
            datetime.strptime(t, "%H:%M") for t in dest_station["departure_times"]
        ]

        for dep_time, arr_time in zip(departure_times, arrival_times):
            if arr_time <= arrival_deadline:
                travel_minutes = int((arr_time - dep_time).total_seconds() // 60)
                return TravelResponse(
                    start=travel.start,
                    destination=travel.destination,
                    time_taken=f"{travel_minutes} minutes (depart at {dep_time.strftime('%H:%M')})",
                    transport="train on Pakenham line",
                )

        return TravelResponse(
            start=travel.start,
            destination=travel.destination,
            time_taken="unknown",
            transport="no valid train found",
        )

    llm_config = {
        "model": "llama3.2",
        "api_type": "ollama",
        "temperature": 0.5,
    }

    trip_request_agent = ConversableAgent(
        name="trip_request_agent",
        system_message="""
        Extract travel details from the user and return ONLY this JSON format:
        {
            "start": {"name": "start_location"},
            "destination": {"name": "destination_location"},
            "time": "arrival_time"
        }
        Return ABSOLUTELY NOTHING else no extra commentary or anything.
        """,
        llm_config=llm_config,
    )

    coordinator = ConversableAgent(
        name="coordinator_agent",
        system_message="Coordinate request and response agents to produce a travel plan.",
        llm_config=llm_config,
    )

    user_inputs = [
        "I want to get to Richmond station by 10:30am from Pakenham Station",
        "Get me to South Yarra by 9:20am from Berwick Station",
        "Reach Narre Warren by 9:05am from East Pakenham Station",
    ]  # different phrasings with/without the station name

    for msg in user_inputs:
        print(f"\nUSER INPUT: {msg}")
        result = coordinator.initiate_chats(
            [{"recipient": trip_request_agent, "message": msg, "max_turns": 1}]
        )
        if result:
            travel_data_str = result[0].summary
        try:
            travel_data = json.loads(travel_data_str)
            travel_request = TravelRequest(**travel_data)
            response = faux_travel_lookup(travel_request)
            print("Travel Response:", response.model_dump())

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
        except Exception as e:
            print(f"Error processing request: {e}")
    else:
        print("Request processed.")

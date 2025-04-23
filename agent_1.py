import json
from pydantic import BaseModel
from autogen import ConversableAgent
from autogen.tools.dependency_injection import BaseContext


class Location(BaseModel):
    name: str
    # future implementation could be lat/long


class TravelRequest(BaseContext, BaseModel):
    start: Location
    destination: Location
    time: str  # departure time


class TravelResponse(BaseContext, BaseModel):
    start: Location
    destination: Location
    time_taken: str
    transport: str  # mode of transport


llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}

trip_request_agent = ConversableAgent(  # declaring agent
    name="request_agent",
    system_message="""
    Extract travel details from the user and return ONLY this JSON format:
    {
        "start": {"name": "start_location"},
        "destination": {"name": "destination_location"},
        "time": "departure_time"
    }
    Return NOTHING else - no text or explanations just the raw JSON.""",  # system prompt to tailor output
    llm_config=llm_config,
)

trip_response_agent = ConversableAgent(
    name="response_agent",
    system_message="""
    Given the travel details, predict the time taken and transport mode in Melbourne, Australia. 
    Format the response as:
    {
        "start": {"name": "start_location"},
        "destination": {"name": "destination_location"},
        "time_taken": "predicted_time_taken",
        "transport": "predicted_transport_mode"
    }
    The time_taken should be a rough estimate of travel time, and the transport mode should be a relevant mode of transport in Melbourne (e.g., tram, train, bus, walking).
    Return NOTHING else - no text or explanations just the raw JSON.""",
    llm_config=llm_config,
)

coordinator = ConversableAgent(
    name="coordinator_agent",
    system_message="Coordinate between request and response agents to generate the complete travel plan for Melbourne, Australia.",
    llm_config=llm_config,  # 'inbetween' agent
)

user_message = "I want to get to Richmond station by 10:30am from Pakenham Station"
"""
user_messages = {
    
}   add more stuff
"""

chat_results = coordinator.initiate_chats(
    [{"recipient": trip_request_agent, "message": user_message, "max_turns": 1}]
)

travel_details = None
if chat_results:
    travel_details = chat_results[0].summary

if travel_details:
    chat_results = coordinator.initiate_chats(
        [{"recipient": trip_response_agent, "message": travel_details, "max_turns": 1}]
    )
    if chat_results:
        print(chat_results[0].summary)
else:
    print("\n\nNo travel details available.")

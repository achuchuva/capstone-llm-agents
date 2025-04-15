import json
import os
from typing import Annotated, Literal
from pydantic import BaseModel
from autogen import GroupChat, GroupChatManager
from autogen.agentchat import ConversableAgent, UserProxyAgent
from autogen.tools.dependency_injection import BaseContext, Depends

class Location(BaseModel):
    name: str
    # coord: Optional[Tuple[float, float]] = None  # more useful for joel and his scheduling bit, figure out how to get data based off names from knowledge base?

class Request(BaseContext, BaseModel):
    start: Location
    destination: Location
    time: str

config_list = [{"api_type": "ollama", "model": "llama3.2"}]

class TravelAgent(ConversableAgent):
    def __init__(self):
        super().__init__(
            name="TravelAgent",
            system_message="""Extract travel details and return ONLY this JSON format:
                            {
                                "start": {"name": "start_location"},
                                "destination": {"name": "destination_location"}, 
                                "time": "departure_time"
                            }
                            Return NOTHING else - no text or explanations just the raw JSON.""",      # NEED TO REWORK PROMPT and maybe put in a separate file
            llm_config={"config_list": config_list},
            human_input_mode="NEVER"            # edit when testing human input
        )

    def _verify(self, data: dict) -> bool:
        """Helper function to verify extracted data meets requirements"""
        required_keys = {"start", "destination", "time"}
        if not all(key in data for key in required_keys):
            return False
        if not isinstance(data["start"], dict) or "name" not in data["start"]:
            return False
        if not isinstance(data["destination"], dict) or "name" not in data["destination"]:
            return False
        return True

def get_request(user_input: str):
    travel_agent = TravelAgent()
    user_proxy = UserProxyAgent(
        "user_proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        max_consecutive_auto_reply=0        # edit 
    )
    user_proxy.initiate_chat(travel_agent, message=user_input, silent=False)
    reply = travel_agent.last_message()['content'].strip()

    if reply.startswith("```"):     # check if starts with code block
        reply = reply.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0].strip() # remove for output cleanliness

    try:
        data = json.loads(reply)
        return Request(
            start=Location(name=data["start"]["name"]),
            destination=Location(name=data["destination"]["name"]),
            time=data["time"],
        )
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Raw reply was: {reply}")
        return None

if __name__ == "__main__":
    request = get_request("I want to get to Glenferrie station by 10:30am from Pakenham Station") # make more examples 
    '''
    requests = {}
    '''
    if request:
        print("Extracted Travel Request:")
        print(f"From: {request.start.name}")
        print(f"To: {request.destination.name}")
        print(f"Time: {request.time}")
    else:
        print("Could not parse request properly :(")        # why is this not working
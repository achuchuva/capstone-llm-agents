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
travel_agent = ConversableAgent(
    name="travel_agent",
    system_message="""Extract travel details and return ONLY this JSON format:
    {
        "start": {"name": "start_location"},
        "destination": {"name": "destination_location"},
        "time": "departure_time"
    }
    Return NOTHING else - no text or explanations just the raw JSON.""",
    description="Agent to extract travel start/destination/time from input",
    llm_config={"config_list": config_list},
)

format_agent = ConversableAgent(
    name="format_agent",
    system_message="""Extract travel details from xx and create text file named travel_plan with this format:
    {
        Head to "start location" to begin your journey,
        You will arive at "destination_location",
        Your departure time is "departure_time"
    }
    Return NOTHING else - no text or explanations just the raw JSON.""",
    description="Agent to format the travel plans from a raw JSON input",
    llm_config={"config_list": config_list},
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    llm_config=False,
    code_execution_config=False,
)

@user_proxy.register_for_execution()
@travel_agent.register_for_llm(description="Parse user input for location and time data")
def travel_request(
    input_text: str,
    context: Annotated[Request, Depends(Request)]
) -> Request:
    return context

groupchat = GroupChat(
    agents=[user_proxy, travel_agent],
    messages=[],
    max_round=5
)
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

if __name__ == "__main__":
    input_message = "I want to get to Glenferrie station by 10:30am from Pakenham Station"

    user_proxy.initiate_chat(manager, message=input_message, max_turns=2)

    print("\nFinal Messages:")
    for msg in groupchat.messages:
        print(f"[{msg['name']}] {msg['content']}")

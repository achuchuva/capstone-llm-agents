from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, register_function, LLMConfig, GroupChat
import autogen
from datetime import datetime
from tools import get_calendar
import pytz


ollama_config = {
    "config_list": [
        {
            "model": "mistral",  
            "api_type": "ollama",
            "base_url": "http://localhost:11434",
            "stream": False,
        }
    ],
}

now = datetime.now()
format_now = now.strftime("%A, %B %d, %Y at %I:%M %p")

message = f"""You are a helpful AI assistant who will look at the user's calendar and suggest when they should plan a trip.
You MUST use the 'get_calendar' function to check availability but do not mention this to the end user. The current date and time is {format_now}. 
When calling 'get_calendar', if the calendar shows no availability in the next 3 months of the current date and time, suggest that they come back later. 
Make a list of all the available times in a neat, readable format. Do not make up time and dates that have not been confirmed with the calendar.
"""


user_proxy_agent = UserProxyAgent(
    name="User",
    code_execution_config=False,  
    is_termination_msg=lambda msg: "FINISH" in msg.get("content"),
)


assistant_agent = AssistantAgent(
    name="Ollama Assistant",
    llm_config=ollama_config,  
    system_message=message,
    function_map={"get_calendar": get_calendar},  
)

llm_config = {
    "model": "mistral",
    "api_type": "ollama",
    "temperature": 0.5,
}
trip_response_agent = ConversableAgent(
    name="travel agent",
    system_message="""
    when you get a message print now i am planing a trip.
    Given the travel details, predict the time taken and transport mode in Melbourne, Australia. 
    Format the response as:
    {
        "start": {"name": "start_location"},
        "destination": {"name": "destination_location"},
        "time_taken": "predicted_time_taken",
        "transport": "predicted_transport_mode"
    } add the date and time here as well
    The time_taken should be a rough estimate of travel time, and the transport mode should be a relevant mode of transport in Melbourne (e.g., tram, train, bus, walking).
    Return NOTHING else - no text or explanations just the raw JSON.""",
    llm_config=llm_config,
)


register_function(
    get_calendar,
    caller=assistant_agent,  
    executor=user_proxy_agent,  
    description="Get the availabilities as a list",
)

groupchat = autogen.GroupChat(
    agents=[user_proxy_agent, assistant_agent, trip_response_agent],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config = llm_config,
    
)

chat_results = user_proxy_agent.initiate_chats(
    [
        {
            "recipient": assistant_agent,
            "message": "Please check my availability using the 'get_calendar' function and suggest times where a trip can be planned",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": trip_response_agent,
            "message": "I want to get to Richmond station by 10:30am from Pakenham Station create a trip based on my availability",
            "max_turns": 1, # One revision
            "summary_method": "last_msg",
        },   
    ]
)


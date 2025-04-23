from autogen import AssistantAgent, UserProxyAgent, ConversableAgent, register_function, LLMConfig, GroupChat
import autogen
from datetime import datetime
from xhtml2pdf import pisa
from tools import get_calendar, create_ics_event, document_creator


granite_config = {
    "model": "granite3.1-dense",
    "api_type": "ollama",
}
llmama_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}
coder_config = {
    "model": "qwen2.5-coder:14b",
    "api_type": "ollama",
}


now = datetime.now()
format_now = now.strftime("%A, %B %d, %Y at %I:%M %p")

message = f"""
You are a helpful AI assistant specializing in managing the user's calendar. Your primary role is to assist the user with scheduling, planning, and organizing their time effectively by interacting with their calendar.

Your responsibilities include:
1.  Checking calendar availability for specific dates, times, or periods based on user requests you must use this function 'get_calendar' to perform this task.
2.  Suggesting suitable available times for activities like planning trips, meetings, or appointments, based on the calendar data you must use this function 'get_calendar' to perform this task.
3.  Adding new events, appointments, or tasks to the calendar when the user provides clear instructions you must first use this function 'get_calendar' then use this function 'create_ics_event' to perform this task.

When checking availability for planning purposes (such as suggesting times for a trip or appointment), if the calendar tool indicates no available slots within the next 3 months from the current date and time ({format_now}), please inform the user that the calendar appears full for that period and they should check back later.
If the planned date and time to add a new event has coincides with another event been, please inform the user that it appears theres already an event planned for that time, and to kindly schedule a different time.
If there are no time clashes, proceed to adding the event to the calendar using this function 'create_ics_event'.
When using this function 'create_ics_event', you must pass in the appropriate format of duration {{"minutes": 60}} or {{"hours": 1}} for example.
Upon successfully updating the calendar, please inform the user politely that the event has been scheduled, along with the details.

Always present available times in a clear, neat, and readable format.
It is critical that you only provide or suggest dates and times that are confirmed as available by the calendar data. Do not make up or infer availability that is not explicitly shown.

Do not mention the specific name of the calendar tool or function you are using to the end user.

The current date and time is {format_now}.
"""
#the user agent for testing
user_proxy_agent = UserProxyAgent(
    name="User",
    code_execution_config=False,  
    human_input_mode="NEVER"
    is_termination_msg=lambda msg: "FINISH" in msg.get("content"),
)

#assitant with access to calander
#can access the .ics file to chekc the calander
assistant_agent = AssistantAgent(
    name="Calander Assitant",
    llm_config=granite_config,  
    system_message=message,
    function_map={"get_calendar": get_calendar, "create_ics_event": create_ics_event},  
)

#replace with whateever the trip response agent is
trip_response_agent = ConversableAgent(
    name="travel agent",
    system_message="""
    when you get a message print now i am planning a trip.
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
    llm_config=llmama_config,
)
#have to play around with the system message to get the desired format this only works with the travel planing agent provided above 
#more genral formats can be added later 
#generates html from the desired output stated in the propmt and creates a pdf using the tool provided to it
documentWriter = ConversableAgent(
    name="Writer Agent",
    system_message="""
    You are a helpful agent that is an expert at generating HTML content for travel reports.

    When you receive a message containing travel details in a dictionary format like:
    {
        "start": {"name": "start_location"},
        "destination": {"name": "destination_location"},
        "time_taken": "predicted_time_taken",
        "transport": "predicted_transport_mode"
        "date & day": "date and day you have planned for"
    }
    AND a list of available dates.

    Your task is to: 
    1. Generate the full HTML content for the report based on this information, using the provided template structure. 
    2. You must call this function 'document_creator' and pass the HTML as the string parameter.
    3. Output what is being passed into the function 'document_creator' as the HTML string, and EXECUTE the function.
    4. After you call the 'document_creator' tool, kindly let the user know of any errors that might occur during the function call.
    
    Template Structure:
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Agent Report</title>
    <style>
      body { font-family: serif; }
      h1 { color: green; }
      p { font-size: 12pt; margin-bottom: 5px;}
      h2, h3 { color: navy; margin-top: 20px; margin-bottom: 10px;}
      ul, ol { margin-bottom: 10px;}
      strong { font-weight: bold; }
    </style>
    </head>
    <body>
        <h2>[Fill Title Here]</h2>
        <ol>
            [Create list items <li> for available dates here]
        </ol>
        <h3>Travel Details:</h3>
        <p><strong>Start Location:</strong> [Fill Start Location Here]</p>
        <p><strong>Destination: </strong> [Fill Destination Here]</p>
        <p><strong>Time Taken: </strong> [Fill Time Taken Here]</p>
        <p><strong>Transport Mode: </strong> [Fill Transport Mode Here]</p>
        <p><strong>Date&Time: </strong> [Fill Date & Time Here]</p>
    </body>
    </html>
    """,
    llm_config=coder_config,
    function_map={"document_creator": document_creator},  
)

register_function(
    get_calendar,
    caller=assistant_agent,  
    executor=user_proxy_agent,  
    description="Get the availabilities as a list",
)

register_function(
    create_ics_event,
    caller=assistant_agent,  
    executor=user_proxy_agent,  
    description="Create and save a calendar event to a .ics file given name, start time, duration (as a dict), and optional location and description",
)

register_function(
    document_creator,
    caller=documentWriter,  
    executor=user_proxy_agent,  
    description="Creates a pdf document from a HTML string",
)

"""
groupchat = autogen.GroupChat(
    agents=[assistant_agent, trip_response_agent, dcoumentWriter],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config = granite_config,  
)
manager.initiate_chat(
    recipient=manager,
    message="Let's start a the discussion!"
)

"""

chat_results = user_proxy_agent.initiate_chats(
    [
        {
            "recipient": assistant_agent,
            #"message": "Please check my availability using the 'get_calendar' function and suggest times where a trip can be planned",
            "message": "Schedule a 45-minute meeting with Jane Doe on Thursday at 3:30 PM to discuss the Q2 marketing strategy. Add it to my work calendar.",
            "max_turns": 2,
            "summary_method": "reflection_with_llm",
        },
         {
            "recipient": assistant_agent,
            "message": "Please check my availability using the 'get_calander' function and suggest times where a trip can be planned",
            "max_turns": 1,
            "summary_method": "last_msg",
        },
        {
            "recipient": trip_response_agent,
            "message": "I want to get to Richmond station by 10:30am from Pakenham Station create a trip based on my availability",
            "max_turns": 1, 
            "summary_method": "last_msg",
        }, 
        {
            "recipient": dcoumentWriter,
            "message": "Please create a document for me",
            "max_turns": 2, 
            "summary_method": "last_msg",
        },   
    ]
)


print("hello\nworld")
from autogen import ConversableAgent


import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta, timezone

from autogen import GroupChat
from autogen import GroupChatManager
import autogen
from autogen import register_function

def plan_formatter(plan: str):
   print("The Plan is")
   print(plan)
   #check if the input is correct. if not return a message telling the LLM to retry otherwise return an array
   result = "error pls try again"
   return result


llm_config = {
    # "model": "gemma3:4b",
    "model": "llama3.2",  # for some reason gemma3 does not have the tools or something to use the functions
    "api_type": "ollama",
    "temperature": 0.5,
}
llm_config2 = {"api_type": "ollama", "model": "gemma3"}

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
   human_input_mode="ALWAYS",
   code_execution_config=False,
   description="A human user capable of working with Autonomous AI Agents.",
)


# https://microsoft.github.io/autogen/0.2/docs/tutorial/chat-termination/ example passing through messages
planner_agent = ConversableAgent(
    name="planner_agent",
    system_message="""
    You are to Create a plan for which agents will be needed and in what order they should be called based on a query. The format should look like this when you use the function. DO NOT FORGET TO START WITH A MESSAGE TO THE NEXT AGENT
    Format to send to the planner_formatter: (Message for the next agent,First agent,Second agent,Third agent,ETC....)

    No other data should be included in this function string only the prompt and a list of each agent you think will help answer the query. Once you have sucesfully returned the array from the formatter function use the call the next agent function.
    The list of agents curently available are {weather_agent, wikipedia_agent, location_agent, history_agent} Do not call more than what is needed""",  #Should change to a vairable string for agent list to make it easier to change
    llm_config=llm_config,
)

weather_agent = ConversableAgent(
    name="weather_agent",
    system_message="""Your Job is to work out the weather of a given location.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

wikipedia_agent = ConversableAgent(
    name="weather_agent",
    system_message="""Your Job is to answer a question based of wikipedia data.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

location_agent = ConversableAgent(
    name="location_agent",
    system_message="""Your Job is to answer questions relating to location.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

history_agent = ConversableAgent(
    name="travel_agent",
    system_message="""Your Job is to answer questions relating to History.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

# https://microsoft.github.io/autogen/0.2/docs/tutorial/tool-use/
# Register the calculator function to the two agents.
register_function(
    plan_formatter,
    caller=planner_agent,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="plan_formatter",  # By default, the function name is used as the tool name.
    description="Used to format a plan of which agents should talk next and with what prompt",  # A description of the tool.
)

user_message = (
    "I want to know what is A horse from wikipedia and if it is raining outside"
)
user_message2 = (
    "I want to know how long it takes to get between pakenham and richmond station in victoria"
)

#user_message3 = input("Enter a query here -->")
#result = location_agent.initiate_chat(weather_agent, message=user_message, max_turns=3)


groupchat = GroupChat(agents=[planner_agent, user_proxy], messages=[], max_round=10)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config2)

user_proxy.initiate_chat(manager, message=user_message)

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

global plan_array#i know global is bad this is just temporaty
plan_array = []


def plan_formatter(new_prompt: str, plan: str):
   print("The new prompt is")
   print(new_prompt)
   print("The Plan is")
   print(plan)
   #check if the input is correct. if not return a message telling the LLM to retry otherwise return an array
   prompt_exists = False
   result = "error no prompt was given. please try again"#default error message
   if new_prompt != "":
      result = "error at least one agent was not found. please try again"#new set error message
      prompt_exists = True
   global plan_array
   plan_array = [new_prompt]
   global agent_list
   agent_order = plan.split(",")
   if prompt_exists == True:#only runs if prompt exists
      for agent_name in agent_order:#grabs the first agent the llm has picked and then the next etc
         print(agent_name.strip())
         agent_found = False
         for agent in agent_list:#checks if the agent exists and if so apends it to the plan array
            if agent.name == agent_name.strip():#strip needed to remove blank spaces
               plan_array.append(agent)
               agent_found = True
         if agent_found == False:
            if agent_name == "":
               error = "You have forgoten to add an agent. please try again with some agents in the plan and do not add any blank ones."
               result = error
               break
            else:
               error = agent_name + " does not exist. please try again."
               result = error
               break
         result = plan_array
   return result


def next_agent():
   global agent_list
   for val in agent_list:
      print("From formated array")
      print(val)
   return "I am the next agent function"


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
    You are to Create a plan for which agents will be needed and in what order they should be called based on a query.
    Format to send to the plan_formatter is: newprompt: generate a prompt plan: agent1,agent2
    No other data should be included in this function string only the new prompt and a list of agents.
    The list of agents curently available are {weather_agent, wikipedia_agent, location_agent, history_agent} Do not call more agents than what is needed""",  #Should change to a vairable string for agent list to make it easier to change
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
    name="wikipedia_agent",
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
    name="history_agent",
    system_message="""Your Job is to answer questions relating to History.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)
#print(history_agent.name)

#list of agents
global agent_list
agent_list = [weather_agent, wikipedia_agent, location_agent, history_agent]
# https://microsoft.github.io/autogen/0.2/docs/tutorial/tool-use/
# Register the calculator function to the two agents.
register_function(
    plan_formatter,
    caller=planner_agent,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="plan_formatter",  # By default, the function name is used as the tool name.
    description="Used to format a plan of which agents should talk next and with what prompt",  # A description of the tool.
)

'''
register_function(
    next_agent,
    caller=planner_agent,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="next_agent",  # By default, the function name is used as the tool name.
    description="Used to create the next chat",  # A description of the tool.
)
'''

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

# the goat
from autogen import ConversableAgent, UserProxyAgent
from autogen import GroupChat
from autogen import GroupChatManager

from pydantic import BaseModel


class PlanStep(BaseModel):
    agent_name: str
    task_prompt: str


class Plan(BaseModel):
    steps: list[PlanStep]


llm_config = {
    "api_type": "ollama",
    "model": "gemma3",
    "response_format": Plan,
}

llm_config_no_plan = {
    "api_type": "ollama",
    "model": "gemma3",
    #"response_format": Plan,
}


user_proxy = UserProxyAgent(
    name="User_proxy",
    human_input_mode="ALWAYS",
    code_execution_config=False,
    description="A human user capable of working with Autonomous AI Agents.",
)

assistant = ConversableAgent(
    name="history_agent",
    system_message="""Your Job is to answer questions relating to History.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

weather_agent = ConversableAgent(
    name="weather_agent",
    system_message="""Your Job is to work out the weather of a given location.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

wikipedia_agent = ConversableAgent(
    name="wikipedia_agent",
    system_message="""Your Job is to answer a question based of wikipedia data.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

location_agent = ConversableAgent(
    name="location_agent",
    system_message="""Your Job is to answer questions relating to location.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

history_agent = ConversableAgent(
    name="history_agent",
    system_message="""Your Job is to answer questions relating to History.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

cooking_agent = ConversableAgent(
    name="cooking_agent",
    system_message="""Your Job is to answer questions relating to cooking.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

ingredients_agent = ConversableAgent(
    name="ingredients_agent",
    system_message="""Your Job is to answer questions relating to ingrients.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

oven_agent = ConversableAgent(
    name="oven_agent",
    system_message="""Your Job is to answer questions relating to overns.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

general_agent = ConversableAgent(
    name="general_agent",
    description="A generic agent used to answer genreal questions such as how are you",
    system_message="""Your Job is to answer questions that are not for a spercific agent such as how are you.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

summary_agent = ConversableAgent(
    name="summary_agent",
    description="A agent used to sumarise all data at the end of a conversation",
    system_message="""Your Job is to summarize the end of a conversation.
    You can make up data if you need.
    """,
    llm_config=llm_config_no_plan,
    human_input_mode="NEVER",  # Never ask for human input.
)

physical_agent_list = [
    oven_agent,
    ingredients_agent,
    cooking_agent,
    wikipedia_agent,
    weather_agent,
    history_agent,
    location_agent,
    general_agent,
]


agents: list = [
    "oven_agent",
    "ingredients_agent",
    "cooking_agent",
    "wikipedia_agent",
    "weather_agent",
    "history_agent",
    "location_agent",
    "general_agent",
    #"summary_agent",Will always add anyway
]


# example

# Give me a recipe to bake a cake


query = "What is the best way to build a 1700s house"

agents_str = ""

for agent in agents:
    agents_str += agent + " "

message = f"""

Create a plan for the following query and select the agents and a necicary prompt for each of them. Use summary agent at the end to summarize what has been said.:

'{query}'

Please use ONLY these agents for the steps. You can use the same agent multiple times. You DO NOT have to use all agents. ONLY USE APPROPRIATE AGENTS.

'{agents_str}'

"""

# example


def generate_plan(query: str) -> Plan:
    response = user_proxy.initiate_chat(assistant, message=query, max_turns=1)

    content = response.summary

    return Plan.model_validate_json(content)


plan = generate_plan(message)

print(plan)


for step in plan.steps:
    print(f"Agent: {step.agent_name}")
    print(f"Task: {step.task_prompt}")
    print()

#obtains all the agents gemma3 recomends plus the summary agent
agents_needed = [summary_agent]
for step in plan.steps:
    agent_needed = str(step.agent_name)
    #print(agent_needed)
    for real_agent in physical_agent_list:
        if agent_needed == real_agent.name:
            agents_needed.append(real_agent)

print(agents_needed)
for agent in agents_needed:
    print(agent.name)

number_of_rounds = len(agents_needed)
#print(number_of_rounds)

prompt = "You are to create a discusion with each of the agents listed once based off what should be prompted to them. You only have " + str(number_of_rounds) + " Rounds of conversation and the last is to be used for the summary agent to sumarise the whole conversaton. The agents and their related prompts should be:\n"
prompt += "The initial prompt you have to answer is " + query + ". And you should follow this rough order\n"
#with both agent and context
'''
for message_pair in plan.steps:
    prompt += ("Agent: " + message_pair.agent_name + " " + "Prompt: " + message_pair.task_prompt + ",\n")
prompt += "Agent: " + summary_agent.name + " " + "Prompt: Summarise what has been discussed in this groupchat."
print(prompt)
'''
#Just with agent list
#'''
for message_pair in plan.steps:
    prompt += ("Agent: " + message_pair.agent_name + ",\n")
prompt += "Agent: " + summary_agent.name + " " + "Final Job: Summarise what has been discussed in this groupchat when you feel is right."
print(prompt)
#'''
groupchat = GroupChat(agents=agents_needed, messages=[], max_round=number_of_rounds)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config_no_plan)

user_proxy.initiate_chat(manager, message=prompt)

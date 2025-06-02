# the goat
from autogen import ConversableAgent, UserProxyAgent

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

cooking_agent = ConversableAgent(
    name="cooking_agent",
    system_message="""Your Job is to answer questions relating to cooking.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

ingredients_agent = ConversableAgent(
    name="ingredients_agent",
    system_message="""Your Job is to answer questions relating to ingrients.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

oven_agent = ConversableAgent(
    name="oven_agent",
    system_message="""Your Job is to answer questions relating to overns.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)

general_agent = ConversableAgent(
    name="general_agent",
    description="A generic agent used to answer genreal questions such as how are you",
    system_message="""Your Job is to answer questions that are not for a spercific agent such as how are you.
    You can make up data if you need.
    """,
    llm_config=llm_config,
    human_input_mode="NEVER",  # Never ask for human input.
)



agents: list = [
    "oven_agent",
    "ingredients_agent",
    "cooking_agent",
    "wikipedia_agent",
    "weather_agent",
    "history_agent",
    "location_agent",
    "general_agent",
]


# example

# Give me a recipe to bake a cake


query = "What is the best way to build a 1700s house"

agents_str = ""

for agent in agents:
    agents_str += agent + " "

message = f"""

Create a plan for the following query and select the agents and a necicary prompt for each of them. Only use the general agent for non spercific querys:

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
    print()  # For spacing between steps

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

agents: list = [
    "oven_agent",
    "ingredients_agent",
    "cooking_agent",
    "wikipedia_agent",
    "weather_agent",
    "history_agent",
]


# example

# Give me a recipe to bake a cake


query = "Give me a recipe to bake cookies"

agents_str = ""

for agent in agents:
    agents_str += agent + " "

message = f"""

Create a plan for the following query:

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

from autogen import AssistantAgent, UserProxyAgent, LLMConfig
from autogen import register_function

print("hello world")
llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}

assistant_agent = AssistantAgent(
    name="Memory Assitant",
    llm_config=llm_config,
    system_message="Your job is to tell the time using the time_calculation function. if you are asked anything that isn't time related don't call the function.",
)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)

def time_calculation(agent_input: str):
    location_time = "The time for " + str(agent_input) + " is 12:00 PM"
    return location_time

register_function(
    time_calculation,
    caller=assistant_agent,
    executor=user_proxy,
    name="time_calculation",  # By default, the function name is used as the tool name.
    description="A function which uses latitude, longditude, date and time to calculate the weather",  # A description of the tool.
)

message = "What is the time for pakenham?."
user_proxy.initiate_chat(
    assistant_agent,
    message=message,
    max_turns=2
)

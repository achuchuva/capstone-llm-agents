from autogen import AssistantAgent, UserProxyAgent, LLMConfig
class scheduling_agent:
  def __init__(self, prompt):
    self.prompt = prompt
    self.test = "test"


test_agent = scheduling_agent("this is the prompt")

print(test_agent.test)
print(test_agent.prompt)


llm_config = LLMConfig.from_json(path="config.json")


with llm_config:
    assistant = AssistantAgent("assistant")

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(
    assistant,
    message="Save a 'message.txt' file with 'Hello world' as its contents.",
    max_turns=2#allows it to move on automanicaly without exit
)

#For testing
print("i got here")

sched_agent = scheduling_agent("this is the prompt to be incerted into the chat automanicaly")
print(sched_agent.test)
print(sched_agent.prompt)


user_proxy.initiate_chat(
    assistant,
    message=input("Enter what you want to tell the prompt:") + ". Now Repeat this prompt all with capital letters.",#i think theres a better way of doing this
)

#will work on better formating and group comunicating tomorow

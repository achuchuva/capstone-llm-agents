from autogen import AssistantAgent, UserProxyAgent, LLMConfig

llm_config = LLMConfig.from_json(path="config.json")


with llm_config:
    assistant = AssistantAgent("assistant")

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)
user_proxy.initiate_chat(
    assistant,
    message="Save a 'message.txt' file with 'Hello world' as its contents.",
)

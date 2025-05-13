from autogen import AssistantAgent, UserProxyAgent, register_function
import sqlite3
import datetime

llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}

assistant_agent = AssistantAgent(
    name="MemoryAssistant",
    llm_config=llm_config,
    system_message="You are to answer any questions to the best of your knowledge. Only save results to your long memory when you know the answer is correct.",
)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)

user_proxy.initiate_chat(
        assistant_agent,
        message="Prompt the assistant agent to be prepared for further questions.",
        max_turns=20,
    )

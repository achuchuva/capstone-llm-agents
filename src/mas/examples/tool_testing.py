"""Module for testing the an agent with tools"""

# TODO remove later just for example testing


import random
from typing import Annotated, Callable

from autogen import GroupChat, GroupChatManager, UserProxyAgent
from app import App
from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_tool import AG2Tool


def get_number_fact(
    number: Annotated[str, "The number to get a fact about"],
) -> str:
    # spoof crash
    crash_chance = 0.5

    random_number = random.random()

    if random_number < crash_chance:
        return "Error: Failed to get fact."

    return f"The number {number} is a very cool number."


def get_number_fact_str_func(app: App) -> Callable[[], str]:

    def func():
        # executor agent
        executor_agent = AG2MASAgent(
            name="ExecutorAgent",
            description="You are an executor agent that executes tools.",
            llm_config=app.config_manager.get_llm_config(use_tools=True),
        )

        agent = AG2MASAgent(
            name="AG2MAS",
            description="Give a fact about a number.",
            llm_config=app.config_manager.get_llm_config(use_tools=True),
        )

        agent.add_tool(
            AG2Tool(
                name="get_number_fact",
                description="Get a fact about a number.",
                func=get_number_fact,
                caller=agent,
                executor=executor_agent,
            )
        )

        agent.register_tools()

        user_proxy = UserProxyAgent(
            name="UserProxyAgent",
            description="You are a user proxy agent that initiates the chat.",
            llm_config=app.config_manager.get_llm_config(use_tools=False),
            human_input_mode="ALWAYS",
            code_execution_config=False,
        )

        group_chat = GroupChat(
            agents=[agent.ag2_agent, executor_agent.ag2_agent],
            max_round=3,
        )

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=app.config_manager.get_llm_config(use_tools=False),
        )

        user_proxy.initiate_chat(
            group_chat_manager,
            message={
                "role": "user",
                "content": "Give me a fact about the number 55.",
            },
            max_turns=1,
        )

        messages = group_chat_manager.groupchat.messages

        last_message = messages[-1]

        content = last_message["content"]

        return content

    return func

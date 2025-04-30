"""Module for testing the an agent with tools"""

# TODO remove later just for example testing


from typing import Annotated

from autogen import GroupChat, GroupChatManager, UserProxyAgent
from app import App
from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_tool import AG2Tool

import requests


def get_number_fact(
    number: Annotated[str, "The number to get a fact about"],
) -> str:
    # using http://numbersapi.com/41

    url = f"http://numbersapi.com/{number}"

    # make a request to the API
    response = requests.get(url, timeout=10)

    # check if the request was successful
    if response.status_code == 200:
        # return the fact
        return response.text

    return "Error: Unable to get a fact about the number."


def test_tool(app: App):
    """Test the task system"""

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

    assistant = AG2MASAgent(
        name="AssistantAgent",
        description="You are an assistant agent.",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
    )

    res = user_proxy.initiate_chat(
        # assistant.ag2_agent,
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

    print(content)

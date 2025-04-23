"""Module for an agent in a MAS using the Autogen2 framework."""

import json
from autogen import ConversableAgent, LLMConfig, register_function
from pydantic import BaseModel

from mas.tool import Tool
from mas.agent import MASAgent


class AG2MASAgent(MASAgent):
    """A class representing an agent in a Multi-Agent System (MAS) using the Autogen2 framework."""

    def __init__(
        self,
        # TODO use AG2Template to build agent, group chat with agents, or swarm
        name: str,
        description: str,
        llm_config: LLMConfig,
        system_message: str | None = None,
        override: bool = True,
        response_format: None | type[BaseModel] = None,
    ):
        """
        Initialise the AG2MASAgent with a name.

        Args:
            name (str): The name of the agent.
            description (str): The description of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            system_message (str | None): The system message for the agent. Defaults to description if None.
            override (bool): Whether to allow recreation of the agent with a new LLM configuration. Defaults to True.
            response_format (None | type[BaseModel]): The response format for the agent. Defaults to None.
        """
        super().__init__(name, description)

        # default to description
        if system_message is None:
            system_message = description

        # copy llm_config
        copy_llm_config: LLMConfig = llm_config.copy()

        response_format: None | type[BaseModel] = response_format or None
        # set response format
        copy_llm_config["response_format"] = response_format

        self.llm_config = copy_llm_config
        """The LLM configuration for the agent."""

        self.response_format = response_format
        """The response format for the agent."""

        self.response_format = response_format
        """The response format for the agent."""

        self.system_message = system_message
        """The system message for the agent."""

        # create ag2 agent
        self.ag2_agent = ConversableAgent(
            name=name,
            description=description,
            system_message=system_message,
            llm_config=copy_llm_config,
        )

        # tools
        self.tools: list[Tool] = []

        self.override = override

    def recreate_llm_config(self):
        """Recreate the LLM configuration for the agent."""

        if not self.override:
            return

        # copy llm_config
        copy_llm_config = self.llm_config.copy()

        # set response format
        copy_llm_config["response_format"] = self.response_format

        self.llm_config = copy_llm_config

    def recreate_agent(self):
        """Recreate the agent with the current LLM configuration."""

        if not self.override:
            return

        # recreate llm config
        self.recreate_llm_config()

        self.ag2_agent = ConversableAgent(
            name=self.name,
            description=self.description,
            system_message=self.system_message,
            llm_config=self.llm_config,
        )

        # register tools
        for tool in self.tools:
            self.register_tool(tool)

    # TODO: This is a hack. It recreates the agent with the new response format.
    # This may have unintended consequences which we are currently unaware of.
    def set_response_format(self, response_format: type[BaseModel]):
        """Set the response format for the agent.

        Args:
            response_format (BaseModel): The response format for the agent.

        """
        self.response_format = response_format

        # recreate agent
        self.recreate_agent()

    def register_tool(self, tool: Tool):
        """Register a tool with the agent.

        Args:
            tool (Tool): The tool to register.
        Raises:
            ValueError: If the tool executor is not an AG2MASAgent.

        """
        # add tool to tools
        self.tools.append(tool)

        executor = tool.get_executor()

        # check if is AG2MASAgent
        if not isinstance(executor, AG2MASAgent):
            raise ValueError(f"Tool executor must be AG2MASAgent, got {type(executor)}")

        register_function(
            f=tool.func,
            caller=self.ag2_agent,
            executor=executor.ag2_agent,
            name=tool.name,
            description=tool.description,
        )

    # TODO you can do multiple prompts in a single call
    # so we need to change it to be a list of prompts
    # and a Prompt obj cause there are settings ({ message: "", role: "user/system" })
    # and a Chat obj cause there are other settings (max_turns, recipient)
    def ask(self, prompt: str, num_tries: int = 1):
        """Prompt the agent.

        Args:
            prompt (str): The prompt to send to the agent.
            num_tries (int): The number of tries to get a response. Defaults to 1.

        """
        # TODO abstract out details

        chat_result = self.ag2_agent.initiate_chat(
            recipient=self.ag2_agent,
            max_turns=num_tries,
            message={
                "role": "user",
                "content": prompt,
            },
        )

        # TODO refactor out to get_last_message() not necessarily .summary
        last_message = chat_result.summary

        # load JSON
        json_data = json.loads(last_message)

        # TODO refactor out response_format

        # convert to pydantic model
        return self.ag2_agent.llm_config["response_format"](**json_data)

    @classmethod
    def from_existing_agent(cls, agent: ConversableAgent):
        """Create an AG2MASAgent from an existing agent.

        Args:
            agent (ConversableAgent): The existing agent to use.

        """

        return cls(
            name=agent.name,
            description=agent.description,
            llm_config=agent.llm_config,
            system_message=agent.system_message,
            override=False,
            response_format=agent.llm_config["response_format"],
        )

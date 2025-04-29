"""Module for a knowledge base agent using the Autogen framework."""

from autogen import ConversableAgent, LLMConfig
from pydantic import BaseModel


class KnowledgeBaseAgent(ConversableAgent):
    """
    A module for an autogen agent that contains a knowledge base.
    """

    def __init__(
        self,
        name: str,
        llm_config: LLMConfig,
        system_message: str | None = None,
        knowledge_base: BaseModel | None = None,
    ):
        """
        Initialise the KnowledgeBaseAgent with a name and knowledge base.

        Args:
            name (str): The name of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            system_message (str | None): The system message for the agent. Defaults to description if None.
            knowledge_base (BaseModel | None): The knowledge base for the agent. Defaults to an empty dictionary.
        """
        super().__init__(
            name,
            llm_config=llm_config,
            human_input_mode="NEVER",
            system_message=system_message,
            code_execution_config=False,
        )
        self.knowledge_base = knowledge_base or {}
        """The knowledge base for the agent."""

    def get_knowledge_base_string(self) -> str:
        """
        Get the knowledge base in string format.

        Returns:
            str: The knowledge base as a string.
        """
        if isinstance(self.knowledge_base, dict):
            return "\n".join(
                [f"{key}: {value}" for key, value in self.knowledge_base.items()]
            )
        return str(self.knowledge_base)

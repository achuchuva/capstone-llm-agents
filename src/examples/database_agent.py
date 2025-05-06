"""Module for autogen agents that expect knowledge bases about a database schema."""

from autogen import ConversableAgent, LLMConfig


class DatabaseAgent(ConversableAgent):
    """
    A module for an autogen agent that contains a knowledge base about a database schema.
    This agent is designed to produce SQL queries based on input and the knowledge base specifying the database structure.
    """

    def __init__(self, name: str, llm_config: LLMConfig, knowledge_base: str):
        """
        Initialise the DatabaseAgent with a name.

        Args:
            name (str): The name of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            knowledge_base (str): The knowledge base for the agent.
        """

        self.knowledge_base = knowledge_base
        system_message = f"""You are a database schema assistant.
            You can construct valid SQL queries that would return results that answer the given prompt.
            Answer ONLY using the following knowledge base:\n\n
            {knowledge_base}\n\n
            If you do not know the answer based on the knowledge base, say 'I'm sorry, I don't have information on that.'
            """

        super().__init__(
            name=name, system_message=system_message, llm_config=llm_config
        )

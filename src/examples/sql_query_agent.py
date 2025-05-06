"""Module for an autogen agent that expects a knowledge base about returned SQL queries."""

from autogen import ConversableAgent, LLMConfig


class SQLQueryAgent(ConversableAgent):
    """
    A module for an autogen agent that contains a knowledge base about arbitrary data returned from an SQL query.
    """

    def __init__(self, name: str, llm_config: LLMConfig, knowledge_base: str):
        """
        Initialise the SQLQueryAgent with a name.

        Args:
            name (str): The name of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            knowledge_base (str): The knowledge base for the agent.
        """

        self.knowledge_base = knowledge_base
        system_message = f"""You are a response formatter assistant.
            You can answer questions by using your knowledge base.
            Assume that the knowledge base is the answer to the query.
            Answer ONLY using the following knowledge base:\n\n
            {knowledge_base}\n\n
            If the question does not match the knowledge base answer at all, say 'I'm sorry, I don't have information on that.'
            ANSWER IN ENGLISH NOT JSON. IF THERE ARE MANY RESULTS, ANSWER IN A TABLE FORMAT.
            """

        super().__init__(
            name=name, system_message=system_message, llm_config=llm_config
        )

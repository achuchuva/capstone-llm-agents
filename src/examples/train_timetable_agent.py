"""Module for an autogen agent that expects a knowledge base about train timetables."""

from autogen import ConversableAgent, LLMConfig


class TrainTimetableAgent(ConversableAgent):
    """
    An (example) module for an autogen agent that contains a knowledge base about train timetables.
    """

    def __init__(self, name: str, llm_config: LLMConfig, knowledge_base: str):
        """
        Initialise the TrainAgent with a name.

        Args:
            name (str): The name of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            knowledge_base (str): The knowledge base for the agent.
        """

        self.knowledge_base = knowledge_base
        print(f"Knowledge base: {knowledge_base}")
        system_message = f"""You are a train timetable assistant. You can answer questions about train timetables.
            Answer ONLY using the following knowledge base:\n\n
            {knowledge_base}\n\n
            If you do not know the answer based on the knowledge base, say 'I'm sorry, I don't have information on that.'
            """

        super().__init__(
            name=name, system_message=system_message, llm_config=llm_config
        )

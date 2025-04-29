"""Module for an autogen agent that contains a knowledge base about train timetables."""

import datetime
from pydantic import BaseModel
from autogen import LLMConfig
from agent.knowledge_base_agent import KnowledgeBaseAgent


class TrainTimetable(BaseModel):
    """
    A class representing a train timetable.
    """

    train_line: str
    """The train line."""
    train_time: str
    """The time of the train."""
    train_destination: str
    """The destination of the train."""

    def __str__(self) -> str:
        """
        Get the string representation of the train timetable.

        Returns:
            str: The string representation of the train timetable.
        """
        return f"Train Line: {self.train_line}, Train Time: {self.train_time}, Train Destination: {self.train_destination}"


class TrainTimetables(BaseModel):
    """
    A class representing a collection of train timetables.
    """

    train_timetables: list[TrainTimetable]
    """A list of train timetables."""

    def __str__(self) -> str:
        """
        Get the string representation of the train timetables.

        Returns:
            str: The string representation of the train timetables.
        """
        return "\n".join([str(timetable) for timetable in self.train_timetables])


class TrainAgent(KnowledgeBaseAgent):
    """
    An (example) module for an autogen agent that contains a knowledge base about train timetables.
    """

    def __init__(
        self, name: str, llm_config: LLMConfig, system_message: str | None = None
    ):
        """
        Initialise the TrainAgent with a name.

        Args:
            name (str): The name of the agent.
            llm_config (LLMConfig): The LLM configuration for the agent.
            system_message (str | None): The system message for the agent. Defaults to description if None.
        """
        # create a knowledge base with train timetables
        knowledge_base = TrainTimetables(
            train_timetables=[
                TrainTimetable(
                    train_line="Hurstbridge",
                    train_time=datetime.datetime(2025, 4, 28, 8, 59).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Hurstbridge",
                    train_time=datetime.datetime(2025, 4, 28, 9, 15).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Hurstbridge",
                    train_time=datetime.datetime(2025, 4, 28, 9, 32).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Hurstbridge",
                    train_time=datetime.datetime(2025, 4, 28, 9, 52).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Hurstbridge",
                    train_time=datetime.datetime(2025, 4, 28, 10, 12).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Pakenham",
                    train_time=datetime.datetime(2025, 4, 28, 8, 56).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Pakenham",
                    train_time=datetime.datetime(2025, 4, 28, 9, 1).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
                TrainTimetable(
                    train_line="Pakenham",
                    train_time=datetime.datetime(2025, 4, 28, 9, 6).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    train_destination="Flinders Street",
                ),
            ]
        )

        super().__init__(name, llm_config, system_message, knowledge_base)

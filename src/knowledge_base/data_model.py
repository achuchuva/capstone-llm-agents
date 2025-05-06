"""
This module contains data models in the form of python classes inheriting from pydantic's BaseModel.
Use model_dump_json() to convert the model into the correct response format (JSON).
"""

import datetime
from pydantic import BaseModel


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


"""Sample data for train timetables"""
train_timetables = TrainTimetables(
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

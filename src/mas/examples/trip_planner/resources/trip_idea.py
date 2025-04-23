"""Module for idea for a trip"""

from pydantic import BaseModel

from mas.base_resource import BaseResource


class TripIdeaResource(BaseResource):
    """A resource representing a trip idea."""

    # city model
    class TripIdeaModel(BaseModel):
        """A model representing a trip idea."""

        city: str
        """The city where the trip idea is located."""
        date: str
        """The date of the trip idea in YYYY-MM-DD format."""
        number_of_activities: int
        """The number of activities in the trip idea."""

    def __init__(self, trip_idea: TripIdeaModel):
        """
        Initialise the TripIdeaResource with a trip idea.

        Args:
            trip_idea (TripIdeaModel): The trip idea to be represented by the resource.
        """
        super().__init__(trip_idea)
        self.trip_idea = trip_idea

    @staticmethod
    def get_model_type() -> type[TripIdeaModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return TripIdeaResource.TripIdeaModel

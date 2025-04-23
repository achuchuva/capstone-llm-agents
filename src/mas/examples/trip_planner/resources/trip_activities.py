"""Activities to do on a trip"""

from pydantic import BaseModel

from mas.base_resource import BaseResource
from mas.examples.trip_planner.resources.activity import ActivityResource


class ActivitiesResource(BaseResource):
    """A resource representing the activities to do on a trip."""

    # itinerary model
    class ActivitiesModel(BaseModel):
        """A model representing the activities to do on a trip."""

        activities: list[ActivityResource.ActivityModel]

    def __init__(self, activities: ActivitiesModel):
        """
        Initialise the ItineraryResource with an itinerary.

        Args:
            activities (ActivitiesModel): The activities to be represented by the resource.
        """
        super().__init__(activities)
        self.activities = activities

    @staticmethod
    def get_model_type() -> type[ActivitiesModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return ActivitiesResource.ActivitiesModel

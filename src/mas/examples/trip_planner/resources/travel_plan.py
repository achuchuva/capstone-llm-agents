"""Travel plan is a list of travels"""

from pydantic import BaseModel

from mas.base_resource import BaseResource
from mas.examples.trip_planner.resources.travel import TravelResource


class TravelPlanResource(BaseResource):
    """A resource representing a travel plan."""

    # travel plan model
    class TravelPlanModel(BaseModel):
        """A model representing a travel plan."""

        travels: list[TravelResource.TravelModel]
        """The travels in the travel plan."""

    def __init__(self, travel_plan: TravelPlanModel):
        """
        Initialise the TravelPlanResource with a travel plan.

        Args:
            travel_plan (TravelPlanModel): The travel plan to be represented by the resource.
        """
        super().__init__(travel_plan)
        self.travel_plan = travel_plan

    @staticmethod
    def get_model_type() -> type[TravelPlanModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return TravelPlanResource.TravelPlanModel

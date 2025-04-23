"""Travel  resource for a travel agent."""

from pydantic import BaseModel

from mas.base_resource import BaseResource


class TravelResource(BaseResource):
    """A resource representing travel between two places."""

    # travel  model
    class TravelModel(BaseModel):
        """A model representing travel between two places."""

        start_location: str
        """The starting location of the travel."""
        end_location: str
        """The ending location of the travel."""
        duration: int
        """The duration of the travel  in minutes."""

    def __init__(self, travel_: TravelModel):
        """
        Initialise the TravelResource with the travel model

        Args:
            travel_ (TravelModel): The travel model to be represented by the resource.
        """
        super().__init__(travel_)
        self.travel_ = travel_

    @staticmethod
    def get_model_type() -> type[TravelModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return TravelResource.TravelModel

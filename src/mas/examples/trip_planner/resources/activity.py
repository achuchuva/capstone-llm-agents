"""An activity to do on a trip"""

from pydantic import BaseModel

from mas.base_resource import BaseResource


class ActivityResource(BaseResource):
    """A resource representing an activity to do on a trip."""

    # activity model
    class ActivityModel(BaseModel):
        """A model representing an activity to do on a trip."""

        location: str
        """The location of the activity."""
        description: str
        """A description of the activity."""

        duration: int
        """The duration of the activity in minutes."""

    def __init__(self, activity: ActivityModel):
        """
        Initialise the ActivityResource with an activity.

        Args:
            activity (ActivityModel): The activity to be represented by the resource.
        """
        super().__init__(activity)
        self.activity = activity

    def __str__(self) -> str:
        """
        Get a string representation of the activity.

        Returns:
            str: A string representation of the activity.
        """
        return (
            self.activity.location + " for " + str(self.activity.duration) + " minutes"
        )

    @staticmethod
    def get_model_type() -> type[ActivityModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return ActivityResource.ActivityModel

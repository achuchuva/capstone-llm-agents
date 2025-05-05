"""Basic text resource class."""

from pydantic import BaseModel


from mas.base_resource import BaseResource


class BoolResource(BaseResource):
    """A resource representing a bool."""

    # bool model
    class BoolModel(BaseModel):
        """A model representing a bool."""

        boolean: bool
        """The text to be represented by the resource."""

        def __init__(self, boolean: bool):
            """
            Initialise the TextModel with a bool.

            Args:
                boolean (bool): The text to be represented by the resource.
            """
            super().__init__(boolean=boolean)
            self.boolean = boolean

    def __init__(self, boolean: BoolModel):
        """
        Initialise the TextResource with a bool.

        Args:
            boolean (bool): The text to be represented by the resource.
        """
        super().__init__(boolean)
        self.boolean = boolean

    @staticmethod
    def get_model_type() -> type[BoolModel]:
        """
        Get the type of the model.

        Returns:
            type: The type of the model.
        """
        return BoolResource.BoolModel

"""Class for communication response"""

from pydantic import BaseModel


class CommunicationResponse:
    """
    A class representing a communication response in a multi-agent system.
    """

    def __init__(self, success: bool, response: BaseModel):
        """
        Initialise a communication response.

        Args:
            success (bool): Indicates whether the response is successful.
            response (BaseModel): The response data.
        """
        self.success = success
        self.response = response

"""Class for communication request"""

from pydantic import BaseModel
from mas.agent import MASAgent


class CommunicationRequest:
    """
    A class representing a communication request in a multi-agent system.
    """

    def __init__(
        self,
        sender: MASAgent,
        receiver: MASAgent,
        message: str,
        response_format: BaseModel,
    ):
        """
        Initialise a communication request.

        Args:
            sender (Agent): The agent sending the request.
            receiver (Agent): The agent receiving the request.
            message (str): The message to be sent.
            response_format (BaseModel): The expected format of the response.
        """
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.response_format = response_format

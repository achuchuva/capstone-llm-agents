"""Module for Communication Protocol."""

from mas.communication.request import CommunicationRequest
from mas.communication.response import CommunicationResponse


class CommunicationProtocol:
    """
    A class defining a communication protocol between agents.
    """

    @staticmethod
    def handle_request(request: CommunicationRequest) -> CommunicationResponse:
        """
        Handle a communication request.

        Args:
            request (CommunicationRequest): The communication request to be handled.

        Returns:
            CommunicationResponse: The response to the communication request.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

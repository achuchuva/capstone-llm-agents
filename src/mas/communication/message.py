"""A message contains the resource, recipient, sender and metadata of the message."""

from mas.agent import MASAgent
from mas.base_resource import BaseResource
from mas.communication.message_metadata import MessageMetadata


class Message:
    """Message class.

    This class contains the resource, recipient, sender and metadata of the message.
    """

    def __init__(
        self,
        resource: BaseResource,
        recipient: MASAgent,
        sender: MASAgent,
        metadata: list[MessageMetadata],
    ) -> None:
        """Initialise the message.

        Args:
            resource (BaseResource): The resource of the message.
            recipient (MASAgent): The recipient of the message.
            sender (MASAgent): The sender of the message.
            metadata (list[MessageMetadata]): The metadata of the message.
        """
        self.resource = resource
        self.recipient = recipient
        self.sender = sender
        self.metadata = metadata

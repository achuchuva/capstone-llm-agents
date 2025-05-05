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
        expected_resource_type: type[BaseResource],
        recipient: MASAgent,
        sender: MASAgent,
        metadata: list[MessageMetadata],
    ) -> None:
        """Initialise the message.

        NOTE: Due to errors within the LLMs or tools, the resource may not be the same type as the expected resource type.

        Args:
            resource (BaseResource): The resource of the message.
            expected_resource_type (type[BaseResource]): The expected resource type of the message.
            recipient (MASAgent): The recipient of the message.
            sender (MASAgent): The sender of the message.
            metadata (list[MessageMetadata]): The metadata of the message.
        """
        self.resource = resource
        """The resource of the message."""
        self.expected_resource_type = expected_resource_type
        """The expected resource type of the message."""
        self.recipient = recipient
        """The recipient of the message."""
        self.sender = sender
        """The sender of the message."""
        self.metadata = metadata
        """The metadata of the message."""

    def add_metadata(self, metadata: MessageMetadata) -> None:
        """Add metadata to the message.

        Args:
            metadata (MessageMetadata): The metadata to add to the message.
        """
        self.metadata.append(metadata)

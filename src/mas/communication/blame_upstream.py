"""Message that blames the upstream agent for the problem."""

from mas.agent import MASAgent
from mas.communication.message import Message
from mas.communication.message_metadata import MessageMetadata
from mas.resources.empty import EmptyResource


class BlameUpstreamMessage(Message):
    """Message that blames the upstream agent for the problem.

    This message is sent to the upstream agent to inform them that there is a problem with the message.
    """

    def __init__(self, sender: MASAgent, upstream_agent: MASAgent):
        """Initialise the blame upstream message.

        Args:
            upstream_agent (MASAgent): The upstream agent that is blamed for the problem.
        """

        # blame upstream metadata
        metadata = MessageMetadata(statement="blame_upstream", relevance_score=1.0)

        super().__init__(
            resource=EmptyResource(EmptyResource.EmptyModel()),
            expected_resource_type=EmptyResource,
            recipient=upstream_agent,
            sender=sender,
            metadata=[metadata],
        )

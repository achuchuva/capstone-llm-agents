"""A decision that the agent made based on the message metrics."""

from mas.communication.decision_enum import DecisionEnum
from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric


class Decision:
    """Decision class.

    This class contains the decision that the agent made based on the message metrics.
    """

    def __init__(
        self,
        metrics: list[MessageMetric],
        message: Message,
        decision_enum: DecisionEnum,
    ) -> None:
        """Initialise the decision.

        Args:
            metrics (list[MessageMetric]): The list of metrics that the agent made the decision on.
            message (Message): The message that the agent made the decision on.
            decision_enum (DecisionEnum): The decision that the agent made based on the message metrics.
        """
        self.metrics = metrics
        """The list of metrics that the agent made the decision on."""
        self.message = message
        """The message that the agent made the decision on."""
        self.decision_enum = decision_enum
        """The decision that the agent made based on the message metrics."""

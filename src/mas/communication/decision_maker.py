"""Decision maker chooses a decision based on the message metrics and the message."""

from mas.communication.decision import Decision
from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric


class DecisionMaker:
    """Decision maker class.

    This class chooses a decision based on the message metrics and the message.
    """

    def make_decision(
        self,
        metrics: list[MessageMetric],
        message: Message,
    ) -> Decision:
        """Make a decision based on the message metrics and the message.

        Args:
            metrics (list[MessageMetric]): The list of metrics that the agent made the decision on.
            message (Message): The message that the agent made the decision on.

        Returns:
            Decision: The decision that the agent made based on the message metrics.
        """
        raise NotImplementedError(
            "make_decision method not implemented in DecisionMaker class. Please implement it in the subclass."
        )

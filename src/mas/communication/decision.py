"""A decision that the agent made based on the message metrics."""

from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric
from mas.communication.problem import Problem


class Decision:
    """Decision class.

    This class contains the decision that the agent made based on the message metrics.
    """

    def __init__(
        self,
        metrics: list[MessageMetric],
        message: Message,
        has_problems: bool,
        known_problems: list[Problem],
    ) -> None:
        """Initialise the decision.

        Args:
            metrics (list[MessageMetric]): The list of metrics that the agent made the decision on.
            message (Message): The message that the agent made the decision on.
            has_problems (bool): Whether the message has problems or not.
            known_problems (list[Problem]): The list of known problems that the message has.
        """
        self.metrics = metrics
        """The list of metrics that the agent made the decision on."""
        self.message = message
        """The message that the agent made the decision on."""
        self.has_problems = has_problems
        """Whether the message has problems or not."""
        self.known_problems = known_problems
        """The list of known problems that the message has."""

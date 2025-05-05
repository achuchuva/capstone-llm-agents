"""Evaluator takes in a message and evaluates on some metrics."""

from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric


class Evaluator:
    """Evaluator class.

    This class evaluates the message based on some metrics.
    """

    def evaluate(self, message: Message) -> list[MessageMetric]:
        """Evaluate the message.
        Args:
            message (Message): The message to evaluate.
        Returns:
            list[MessageMetric]: The list of metrics to evaluate the message.
        """

        raise NotImplementedError(
            "evaluate method not implemented in Evaluator class. Please implement it in the subclass."
        )

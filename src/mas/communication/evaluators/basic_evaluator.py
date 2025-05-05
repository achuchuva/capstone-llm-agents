"""Basic evaluator will evaluate a message on two metrics: accuracy and relevance."""

from mas.communication.evaluator import Evaluator
from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric


class BasicEvaluator(Evaluator):
    """Basic evaluator class.

    This class evaluates the message based on two metrics: accuracy and relevance.
    """

    def _evaluate_accuracy(self, message: Message) -> MessageMetric:
        """Evaluate the accuracy of the message.

        Args:
            message (Message): The message to evaluate.

        Returns:
            MessageMetric: The accuracy metric of the message.
        """
        # TODO placeholder, how it should work is to check if the message data matches the expected data
        # and just return 0 or 1
        accuracy_value = 0.95
        accuracy_metric = MessageMetric("accuracy", accuracy_value)

        return accuracy_metric

    def _evaluate_relevance(self, message: Message) -> MessageMetric:
        """Evaluate the relevance of the message.

        Args:
            message (Message): The message to evaluate.

        Returns:
            MessageMetric: The relevance metric of the message.
        """
        # TODO placeholder, how it should work is it should ask the LLM if the message is relevant to the user task
        # and just return 0 or 1
        relevance_value = 0.85
        relevance_metric = MessageMetric("relevance", relevance_value)

        return relevance_metric

    def evaluate(self, message: Message) -> list[MessageMetric]:
        """Evaluate the message.

        Args:
            message (Message): The message to evaluate.

        Returns:
            list[MessageMetric]: The list of metrics to evaluate the message.
        """

        accuracy = self._evaluate_accuracy(message)
        relevance = self._evaluate_relevance(message)

        return [accuracy, relevance]

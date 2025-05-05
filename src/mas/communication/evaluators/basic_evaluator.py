"""Basic evaluator will evaluate a message on two metrics: accuracy and relevance."""

from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_task import AG2Task
from mas.communication.evaluator import Evaluator
from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric
from mas.resources.bool import BoolResource
from mas.resources.empty import EmptyResource


class BasicEvaluator(Evaluator):
    """Basic evaluator class.

    This class evaluates the message based on two metrics: accuracy and relevance.
    """

    def __init__(self, relevance_checker: AG2MASAgent) -> None:
        """Initialise the basic evaluator.

        Args:
            relevance_checker (AG2MASAgent): The relevance checker agent.
        """
        super().__init__()
        self.relevance_checker = relevance_checker
        """The relevance checker agent."""

    def _evaluate_accuracy(self, message: Message) -> MessageMetric:
        """Evaluate the accuracy of the message.

        Args:
            message (Message): The message to evaluate.

        Returns:
            MessageMetric: The accuracy metric of the message.
        """

        def is_accurate(message: Message) -> bool:
            """Check if the message is accurate.

            Args:
                message (Message): The message to check.

            Returns:
                bool: True if the message is accurate, False otherwise.
            """
            return isinstance(message.resource, message.expected_resource_type)

        accuracy_metric = MessageMetric(
            "accuracy",
            float(int(is_accurate(message))),
        )

        return accuracy_metric

    def _evaluate_relevance(self, message: Message) -> MessageMetric:
        """Evaluate the relevance of the message.

        Args:
            message (Message): The message to evaluate.

        Returns:
            MessageMetric: The relevance metric of the message.
        """
        # TODO placeholder, how it should work is it should ask the LLM if the message is relevant to the user task

        def is_relevant(message: Message) -> bool:
            """Check if the message is relevant.

            Args:
                message (Message): The message to check.

            Returns:
                bool: True if the message is relevant, False otherwise.
            """

            recipient = message.recipient

            recipient_description = recipient.description

            # create a prompt to ask the LLM if the message is relevant
            prompt = f"Is this resource '{message.resource.model}' relevant to the recipient '{recipient_description}'?"

            task = AG2Task(
                name="Check relevance",
                description="Check if the message is relevant to the recipient",
                input_resource=EmptyResource,
                output_resource=BoolResource,
                generate_str=lambda x: prompt,
                agent=self.relevance_checker,
            )

            response = task.do(EmptyResource(EmptyResource.EmptyModel()))

            # if it messes up then assume that its not relevant

            if not isinstance(response, BoolResource):
                return False

            return response.boolean.boolean

        # and just return 0 or 1
        relevance_metric = MessageMetric("relevance", float(int(is_relevant(message))))

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

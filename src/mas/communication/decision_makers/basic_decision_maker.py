"""Basic decision maker proceeds with accurate and relevant messages and otherwise rejects them."""

from mas.communication.decision import Decision

from mas.communication.decision_enum import DecisionEnum

from mas.communication.decision_maker import DecisionMaker

from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric


class BasicDecisionMaker(DecisionMaker):
    """Basic decision maker class.

    This class proceeds with accurate and relevant messages and otherwise rejects them.
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

        # get the accuracy and relevance metrics
        accuracy_metric = next(
            metric for metric in metrics if metric.name == "accuracy"
        )
        relevance_metric = next(
            metric for metric in metrics if metric.name == "relevance"
        )

        # if the accuracy and relevance metrics are not present, return a default decision
        if accuracy_metric is None or relevance_metric is None:
            return Decision(
                metrics,
                message,
                DecisionEnum.REJECT,
            )

        # otherwise we make a decision based on the accuracy and relevance metrics

        # somewhat accurate and relevant, we proceed
        is_accurate = accuracy_metric.value >= 0.5
        is_relevant = relevance_metric.value >= 0.5

        if is_accurate and is_relevant:
            decision_enum = DecisionEnum.PROCEED
        else:
            decision_enum = DecisionEnum.REJECT

        return Decision(metrics, message, decision_enum)

"""Basic decision maker proceeds with accurate and relevant messages and otherwise rejects them."""

from mas.communication.decision import Decision

from mas.communication.decision_maker import DecisionMaker

from mas.communication.message import Message
from mas.communication.message_metric import MessageMetric
from mas.communication.problem import Problem


class BasicDecisionMaker(DecisionMaker):
    """Basic decision maker class.

    This class proceeds with accurate and relevant messages and otherwise rejects them.
    """

    def __init__(self, known_problems: list[Problem]) -> None:
        """Initialise the basic decision maker.

        Args:
            problems (list[Problem]): The list of known problems that the message has.
        """
        super().__init__()
        self.known_problems = known_problems

    # TODO abstract this out to a base class
    def message_has_good_metrics(
        self,
        metrics: list[MessageMetric],
    ) -> bool:
        """Check if the message has good metrics.

        Args:
            metrics (list[MessageMetric]): The list of metrics that the agent made the decision on.
        Returns:
            bool: Whether the message has good metrics or not.
        """
        # get the accuracy and relevance metrics
        accuracy_metric = next(
            metric for metric in metrics if metric.name == "accuracy"
        )
        relevance_metric = next(
            metric for metric in metrics if metric.name == "relevance"
        )

        # if we don't have the metrics, we then obviously don't have good metrics
        if accuracy_metric is None or relevance_metric is None:
            return False

        # somewhat accurate and relevant, we proceed
        is_accurate = accuracy_metric.value >= 0.5
        is_relevant = relevance_metric.value >= 0.5

        return is_accurate and is_relevant

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

        # TODO how to handle if metrics are bad?
        # no metrics, we blame the sender (kind of arbitrary)
        if self.message_has_good_metrics(metrics):
            return Decision(
                metrics,
                message,
                False,
                [],
            )

        # otherwise we need to find the problems
        problems = []

        for problem in self.known_problems:
            if problem.caused_by_metrics(metrics):
                problems.append(problem)

        return Decision(
            metrics,
            message,
            True,
            problems,
        )

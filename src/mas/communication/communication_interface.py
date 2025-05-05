"""An interface a particular agent's communication method with other agents within the MAS."""

from mas.communication.decision_handler import DecisionHandler
from mas.communication.decision_maker import DecisionMaker
from mas.communication.evaluator import Evaluator
from mas.communication.message import Message


class CommunicationInterface:
    """Communication interface class.

    This class is an interface for a particular agent's communication method with other agents within the MAS.
    """

    def __init__(
        self,
        handler: DecisionHandler,
        evaluator: Evaluator,
        decision_maker: DecisionMaker,
    ) -> None:
        """Initialise the communication interface.

        Args:
            handler (DecisionHandler): Decides which checkpoint and what message to send to the checkpoint to resume communication.
            evaluator (Evaluator): The evaluator that the agent uses to evaluate the message metrics.
            decision_maker (DecisionMaker): The decision maker that the agent uses to make a decision based on the message metrics and the message.
        """
        self.handler = handler
        """The decision handler that the agent uses to decide which checkpoint and what message to send to the checkpoint to resume communication."""
        self.evaluator = evaluator
        """The evaluator that the agent uses to evaluate the message metrics."""
        self.decision_maker = decision_maker
        """The decision maker that the agent uses to make a decision based on the message metrics and the message."""

    def handle_message(self, message: Message) -> Message:
        """Handle the message.

        Args:
            message (Message): The message to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """

        # first evaluate the message
        metrics = self.evaluator.evaluate(message)

        # then make a decision based on the message metrics
        decision = self.decision_maker.make_decision(metrics, message)

        # then handle the decision
        return self.handler.handle_decision(decision)

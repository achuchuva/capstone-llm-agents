"""Decision handler decides which checkpoint and what message to send to the checkpoint to resume communication."""

from mas.communication.checkpoint import Checkpoint
from mas.communication.decision import Decision
from mas.communication.message import Message


class DecisionHandler:
    """Decision handler class.

    This class decides which checkpoint and what message to send to the checkpoint to
    resume communication.
    """

    def __init__(self, checkpoint: Checkpoint) -> None:
        """Initialise the decision handler.

        Args:
            checkpoint (Checkpoint): The checkpoint that the agent is at.
        """
        self.checkpoint = checkpoint
        """The checkpoint that the agent is at."""

    def handle_decision(self, decision: Decision) -> Message:
        """Handle the decision.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        raise NotImplementedError(
            "handle_decision method not implemented in DecisionHandler class. Please implement it in the subclass."
        )

    def _handle_decision_with_no_problems(self, decision: Decision) -> Message:
        """Handle the decision that appears to have no problems.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        raise NotImplementedError(
            "_handle_decision_with_no_problems method not implemented in DecisionHandler class. Please implement it in the subclass."
        )

    def _handle_decision_with_known_problems(self, decision: Decision) -> Message:
        """Handle the decision with appears to have some known problems.
        For now this could be a hard-coded list of problems, but later could be dynamically generated or fetched from long-term memory even.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        raise NotImplementedError(
            "_handle_decision_with_known_problems method not implemented in DecisionHandler class. Please implement it in the subclass."
        )

    def _handle_decision_with_unknown_problems(self, decision: Decision) -> Message:
        """Handle the decision with appears to have a problem or problems that are not known.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        raise NotImplementedError(
            "_handle_decision_with_unknown_problems method not implemented in DecisionHandler class. Please implement it in the subclass."
        )

    def handle_decision_upstream(self, decision: Decision) -> Message:
        """Send the message upstream.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        raise NotImplementedError(
            "handle_decision_upstream method not implemented in DecisionHandler class. Please implement it in the subclass."
        )
        # TODO send the message upstream to the previous checkpoint

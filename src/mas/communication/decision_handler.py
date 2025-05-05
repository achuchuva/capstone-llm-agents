"""Decision handler decides which checkpoint and what message to send to the checkpoint to resume communication."""

from mas.communication.checkpoint import Checkpoint
from mas.communication.decision import Decision
from mas.communication.message import Message


class DecisionHandler:
    """Decision handler class.

    This class decides which checkpoint and what message to send to the checkpoint to
    resume communication.
    """

    def __init__(self, checkpoints: list[Checkpoint]) -> None:
        """Initialise the decision handler.

        Args:
            checkpoints (list[Checkpoint]): The list of checkpoints that the decision handler can pass to.
        """
        self.checkpoints = checkpoints
        """The list of checkpoints."""

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

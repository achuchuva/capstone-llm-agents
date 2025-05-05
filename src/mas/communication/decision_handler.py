"""Decision handler decides which checkpoint and what message to send to the checkpoint to resume communication."""

from mas.communication.checkpoint import Checkpoint


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

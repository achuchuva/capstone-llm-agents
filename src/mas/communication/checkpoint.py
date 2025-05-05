"""Checkpoint class for important stages within the MAS."""

from mas.agent import MASAgent


class Checkpoint:
    """Checkpoint class for important stages within the MAS."""

    def __init__(self, agent: MASAgent) -> None:
        """Initialise the checkpoint.

        Args:
            agent (MASAgent): The agent at the checkpoint.
        """
        self.agent = agent
        """The agent that created the checkpoint."""

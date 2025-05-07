"""Communication protocol for the MAS."""

from mas.communication.checkpoint import Checkpoint


class CommunicationProtocol:
    """Communication protocol for the MAS."""

    checkpoints: list[Checkpoint]
    """List of checkpoints in the communication protocol."""

    def __init__(self):
        """
        Initialise the communication protocol.
        """
        self.checkpoints = []

        self.checkpoint_index = 0
        """Index of the current checkpoint in the communication protocol."""

    def add_checkpoint(self, checkpoint: Checkpoint):
        """Add a checkpoint to the communication protocol.

        Args:
            checkpoint (Checkpoint): The checkpoint to be added to the communication protocol.
        """
        self.checkpoints.append(checkpoint)

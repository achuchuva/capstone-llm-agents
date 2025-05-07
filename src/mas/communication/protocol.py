"""Communication protocol for the MAS."""

from mas.agent import MASAgent
from mas.communication.checkpoint import Checkpoint
from mas.communication.message import Message
from mas.horn_clause import HornClause
from mas.query.query_plan import QueryPlan
from mas.resources.empty import EmptyResource


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

    def could_not_satisfy_query(self) -> bool:
        """Check if the communication protocol has failed to satisfy the query.

        Returns:
            bool: True if the communication protocol has failed, False otherwise.
        """
        # TODO
        # check if we have failed at the checkpoint n times
        return False

    def add_checkpoint(self, checkpoint: Checkpoint):
        """Add a checkpoint to the communication protocol.

        Args:
            checkpoint (Checkpoint): The checkpoint to be added to the communication protocol.
        """
        self.checkpoints.append(checkpoint)

    def wrap(self, clause: HornClause) -> Message:
        """Wrap the clause in a message.

        Args:
            clause (HornClause): The clause to be wrapped up.
        Returns:
            Message: The message that the clause is wrapped in.
        """
        # TODO

        # unknown agent
        unknown_agent = MASAgent(
            name="unknown",
            description="unknown",
        )

        message = Message(
            resource=EmptyResource(EmptyResource.EmptyModel()),
            expected_resource_type=EmptyResource,
            recipient=unknown_agent,
            sender=unknown_agent,
            metadata=[],
        )

        return message

    def handle_message(self, message: Message) -> Message:
        """Handle the message through the communication protocol.

        Args:
            message (Message): The message to be handled.
        Returns:
            Message: The new message after it has been handled.
        """
        # TODO
        return message

    def alter_plan(
        self, plan: QueryPlan, step: int, message: Message
    ) -> tuple[QueryPlan, int]:
        """Alter the plan based on the message.

        Args:
            plan (QueryPlan): The plan to be altered.
            step (int): The current step in the plan.
            message (Message): The message to be handled.
        Returns:
            tuple[QueryPlan, int]: The new plan and the index of where to resume the plan.
        """
        # TODO solutions should update the plan
        return plan, step

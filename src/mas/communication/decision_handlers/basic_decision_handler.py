"""The basic decision handler will use the current if proceeding, and will reject to the first checkpoint if rejecting."""

from mas.communication.decision_enum import DecisionEnum
from mas.communication.decision_handler import DecisionHandler

from mas.communication.decision import Decision

from mas.communication.message import Message


class BasicDecisionHandler(DecisionHandler):
    """Basic decision handler class.

    This class is a basic implementation of the decision handler that uses the current
    checkpoint if proceeding, and rejects to the first checkpoint if rejecting.
    """

    def handle_decision(self, decision: Decision) -> Message:
        """Handle the decision.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        if decision.decision_enum == DecisionEnum.PROCEED:
            return decision.message

        # first checkpoint
        checkpoint = self.checkpoints[0]

        if checkpoint is None:
            raise ValueError("No checkpoint available to reject to.")

        # reject to the first checkpoint
        checkpoint_agent = checkpoint.agent

        # TODO assumes that the resource is valid
        # TODO this is assumes a lot of stuff, like no metadata, and that this is a valid request

        # TODO I think in reality the checkpoint agent would need to be passed in the decision and/or feedback
        # and generate a new message based on that

        return Message(
            resource=decision.message.resource,
            expected_resource_type=decision.message.expected_resource_type,
            recipient=checkpoint_agent,
            sender=decision.message.sender,
            metadata=[],
        )

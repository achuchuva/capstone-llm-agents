"""The basic decision handler will use the current if proceeding, and will reject to the first checkpoint if rejecting."""

from mas.communication.decision_handler import DecisionHandler

from mas.communication.decision import Decision

from mas.communication.message import Message


class BasicDecisionHandler(DecisionHandler):
    """Basic decision handler class.

    This class is a basic implementation of the decision handler that uses the current
    checkpoint if proceeding, and rejects to the first checkpoint if rejecting.
    """

    def _handle_incoming_upstream_blame(self, decision: Decision) -> Message:
        """Handle the decision that is blamed on us as the upstream agent.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        # TODO for now we will just send upstream again
        return self.handle_decision_upstream(decision)

    def _handle_decision_with_no_problems(self, decision: Decision) -> Message:
        """Handle the decision that appears to have no problems.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        return decision.message

    def _handle_decision_with_known_problems(self, decision: Decision) -> Message:
        """Handle the decision with appears to have some known problems.
        For now this could be a hard-coded list of problems, but later could be dynamically generated or fetched from long-term memory even.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        # TODO default will be to try solutions for each problem one by one

        # lets make a big assumption that there will be only one problem
        # if the first problem solution does not work, we will try the next solution

        # TODO for now we will just send upstream
        return self.handle_decision_upstream(decision)

    def _handle_decision_with_unknown_problems(self, decision: Decision) -> Message:
        """Handle the decision with appears to have a problem or problems that are not known.

        Args:
            decision (Decision): The decision to handle.

        Returns:
            Message: The message that the agent sent to the checkpoint.
        """
        return self.handle_decision_upstream(decision)

    def handle_decision_upstream(self, decision: Decision) -> Message:
        """Send the message upstream.
        Args:
            decision (Decision): The decision to handle.
        Returns:
            Message: The message that the agent sent to the checkpoint.
        """

        # find the first checkpoint
        checkpoint = self.checkpoint

        if checkpoint is None:
            raise ValueError("No checkpoint available to send upstream to.")

        # some default message that just says that we had some unknown problem we couldn't solve

        # TODO make a special message for this
        # TODO therefore we need a special checkpoint agent that can handle this
        # or the checkpoint itself can handle this, so we dont have to do weird multi-inheritance with agents

        message = decision.message

        message = Message(
            resource=message.resource,
            expected_resource_type=message.expected_resource_type,
            recipient=checkpoint.agent,
            sender=message.sender,
            metadata=[],
        )

        return message

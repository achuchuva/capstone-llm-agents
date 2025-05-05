"""Decision enum for MAS communication."""

from enum import Enum


class DecisionEnum(Enum):
    """Decision enum for MAS communication.

    This enum contains the possible decisions that the agent can make for a message request.
    """

    PROCEED = "PROCEED"
    """The agent decides to proceed with the message request."""

    REJECT = "REJECT"
    """The agent does not know how to handle the message request."""

    ASK_FOR_CLARIFICATION = "CLARIFY"
    """The agent ask to clarify / fix aspects of the message request."""

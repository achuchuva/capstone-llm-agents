"""Decision enum for MAS communication."""

from enum import Enum


class DecisionEnum(Enum):
    """Decision enum for MAS communication.

    This enum contains the possible decisions that the agent can make for a message request.
    """

    PROCEED = "PROCEED"
    """The agent decides to proceed with the message request."""

    BLAME = "BLAME"
    """The agent decides to blame the sender of the message request, asking them to fix the message request."""

    TRY_TO_FIX = "TRY_TO_FIX"
    """The agent decides to try to fix the message request."""

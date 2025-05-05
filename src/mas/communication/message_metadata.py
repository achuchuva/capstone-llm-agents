"""Message metadata module."""

# TODO make more flexible, won't necessarily be a string


class MessageMetadata:
    """Message metadata class.

    This class contains the metadata of a message, including the sender, recipient,
    and timestamp.
    """

    def __init__(self, statement: str, relevance_score: float) -> None:
        """Initialise the message metadata.

        Args:
            statement (str): The statement of the message.
            relevance_score (float): The relevance score of the message.
        """
        self.statement = statement
        self.relevance_score = relevance_score

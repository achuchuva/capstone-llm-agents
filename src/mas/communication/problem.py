"""A known problem that the message has."""

from mas.communication.message_metric import MessageMetric


class Problem:
    """Problem class.

    This class contains the problem that the message has.
    """

    def __init__(self, name: str, description: str) -> None:
        """Initialise the problem.

        Args:
            name (str): The name of the problem.
            description (str): The description of the problem.
        """
        self.name = name
        """The name of the problem."""
        self.description = description
        """The description of the problem."""

    # caused by metrics
    def caused_by_metrics(self, metrics: list[MessageMetric]) -> bool:
        """Whether the problem is caused by metrics or not.

        Returns:
            bool: Whether the problem is caused by metrics or not.
        """
        raise NotImplementedError(
            "caused_by_metrics method not implemented in Problem class. Please implement it in the subclass."
        )

"""A metric to evaluate the state of a message."""


class MessageMetric:
    """Message metric class.

    This class contains the metric of a message.
    """

    def __init__(self, name: str, value: float) -> None:
        """Initialise the message metric.

        Args:
            name (str): The name of the metric.
            value (float): The value of the metric.
        """
        self.name = name
        self.value = value

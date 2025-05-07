"""A known problem that the message has."""

from mas.communication.message_metric import MessageMetric
from mas.communication.message import Message


class Problem:
    """Problem class.

    This class contains the problem that the message has.
    """

    def __init__(self, name: str, description: str, known_solution: "Solution") -> None:
        """Initialise the problem.

        Args:
            name (str): The name of the problem.
            description (str): The description of the problem.
        """
        self.name = name
        """The name of the problem."""
        self.description = description
        """The description of the problem."""

        # known solution
        self.known_solution = known_solution
        """The known solution to the problem."""

    # caused by metrics
    def caused_by_metrics(self, metrics: list[MessageMetric]) -> bool:
        """Whether the problem is caused by metrics or not.

        Returns:
            bool: Whether the problem is caused by metrics or not.
        """
        raise NotImplementedError(
            "caused_by_metrics method not implemented in Problem class. Please implement it in the subclass."
        )


# TODO circular dependency, refactor ideally
class Solution:
    """Solution class.

    This class contains the solution to a problem in the message.
    """

    def __init__(
        self,
        name: str,
        description: str,
    ):
        """Initialise the solution.

        Args:
            name (str): The name of the solution.
            description (str): The description of the solution.
        """
        self.name = name
        """The name of the solution."""
        self.description = description
        """The description of the solution."""

    def generate_solution_message(
        self,
        message: Message,
        problem: Problem,
    ) -> Message:
        """Generate a solution message.

        Args:
            message (Message): The message that that has the problem.
            problem (Problem): The problem that the solution is trying to solve.
        Returns:
            Message: The solution message.
        """

        raise NotImplementedError(
            "The generate_solution_message method is not implemented in the Solution class."
        )

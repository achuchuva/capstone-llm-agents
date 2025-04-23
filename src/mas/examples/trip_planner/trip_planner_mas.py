"""MAS for planning trips"""

from mas.multi_agent_system import MultiAgentSystem
from mas.resource_alias import ResourceAlias
from mas.resources.empty import EmptyResource
from mas.task import Task


class TripPlannerMAS(MultiAgentSystem):
    """Trip Planner MAS"""

    def __init__(self):
        """
        Initialise the Trip Planner MAS.
        """

        # add the agents

        # resource aliases
        alias = ResourceAlias()

        # add the resources
        alias.add_resource_alias("empty", EmptyResource)

        # add the tasks
        tasks: list[Task] = []

        for task in tasks:
            self.add_task(task)

        super().__init__(alias)

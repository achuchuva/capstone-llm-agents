"""Runs the plan for a given query"""

from mas.base_resource import BaseResource
from mas.clauses.horn_descriptor import HornClauseForDepedendentDescriptor
from mas.clauses.horn_resource_assignment import HornClauseForResourceAssignment
from mas.clauses.horn_task import HornClauseForTask
from mas.horn_clause import HornClause
from mas.query.query_plan import QueryPlan
from mas.resource_manager import ResourceManager
from mas.task import Task


class PlanRunner:
    """Runs the plan for a given query."""

    def __init__(
        self,
        query_plan: QueryPlan,
        resource_manager: ResourceManager,
        input_resources: dict[tuple[type[BaseResource], int], BaseResource],
        output_resource_tuple: tuple[type[BaseResource], int],
        # communnication protocol (checkpoints)
    ):
        """
        Initialise the QueryRunner with a query plan and resource manager.

        Args:
            query_plan (QueryPlan): The query plan to be executed
            resource_manager (ResourceManager): The resource manager for the MAS
            input_resources (dict[tuple[type[BaseResource], int], BaseResource]): The input resources for the query
            output_resource_tuple (tuple[type[BaseResource], int]): The output resource tuple for the query
        """
        self.query_plan = query_plan
        self.resource_manager = resource_manager

        # lookup for resource values
        self.resource_values: dict[tuple[type[BaseResource], int], BaseResource] = {}

        # add input resources
        # TODO its not a copy which is a problem, should be fine though I think
        # because each task generates a new resource
        for resource_tuple, resource in input_resources.items():
            self.resource_values[resource_tuple] = resource

        self.output_resource_tuple = output_resource_tuple

        self.step = 0
        """Step in the query plan."""

    def get_next_step(self) -> HornClause:
        """
        Get the next step in the query plan.

        Returns:
            HornClause: The next step in the query plan
        """
        if self.step >= len(self.query_plan.horn_clauses):
            raise ValueError("Query plan is complete.")

        return self.query_plan.horn_clauses[self.step]

    def run_next_step(self) -> None:
        """
        Run the next step in the query plan.
        """

        # get next clause
        clause = self.query_plan.horn_clauses[self.step]

        # run clause
        self.run_clause(clause)

        # increment step
        self.step += 1

    def complete(self) -> bool:
        """
        Check if the query plan is complete.

        Returns:
            bool: True if the query plan is complete, False otherwise
        """
        return self.step >= len(self.query_plan.horn_clauses)

    def run(self) -> BaseResource:
        """
        Run the query plan.

        Returns:
            None
        """

        # iter over clauses
        for clause in self.query_plan.horn_clauses:
            print("Running clause", clause)
            # run clause
            self.run_clause(clause)

        # lookup output resource
        return self.get_final_resource()

    def get_final_resource(self) -> BaseResource:
        """
        Get the final resource after running the query plan.

        Returns:
            BaseResource: The final resource after running the query plan
        """
        if self.output_resource_tuple not in self.resource_values:
            raise ValueError(
                f"Plan did not have output resource {self.output_resource_tuple} in resource values."
            )

        return self.resource_values[self.output_resource_tuple]

    def run_clause(self, clause: HornClause) -> None:
        """
        Run a clause in the query plan.
        Args:
            clause (HornClause): The clause to be run
        """

        # get input and output resource tuples
        input_resource_tuple, output_resource_tuple = (
            self.get_input_output_tuple_from_clause(clause)
        )

        # get input resource
        input_resource = self.resource_values.get(input_resource_tuple)

        if input_resource is None:
            raise ValueError(
                f"Plan did not have input resource {input_resource_tuple} in resource values."
            )

        # get task
        if isinstance(clause, HornClauseForResourceAssignment):
            # e.g. sentence_0 => sentence_2
            self.resource_values[output_resource_tuple] = input_resource

        else:
            # get task
            task = self.get_task_from_clause(clause)

            # run task
            output_resource = self.run_task(task, input_resource, output_resource_tuple)

            # set output resource
            self.resource_values[output_resource_tuple] = output_resource

    def run_task(
        self,
        task: Task,
        input_resource: BaseResource,
        output_resource_tuple: tuple[type[BaseResource], int],
    ) -> BaseResource:
        """
        Run a task.

        Args:
            task (Task): The task to be run
            input_resource (BaseResource): The input resource for the task
            output_resource_tuple (tuple[type[BaseResource], int]): The output resource tuple for the task

        Returns:
            BaseResource: The output resource for the task
        """
        # run task
        output_resource = task.do(input_resource)

        # set output resource
        self.resource_values[output_resource_tuple] = output_resource

        return output_resource

    def get_input_output_tuple_from_clause(
        self, clause: HornClause
    ) -> tuple[tuple[type[BaseResource], int], tuple[type[BaseResource], int]]:
        """
        Get the input and output resource tuples from a clause.
        Args:
            clause (HornClause): The clause to get the input and output resource tuples from
        Returns:
            tuple[tuple[type[BaseResource], int], tuple[type[BaseResource], int]]: The input and output resource tuples
        """

        # handle type
        if isinstance(clause, HornClauseForDepedendentDescriptor):
            # e.g. topic_1 => about_topic(sentence_1)
            return (
                clause.dependent_task.input_resource_tuple,
                clause.dependent_task.output_resource_tuple,
            )

        elif isinstance(clause, HornClauseForResourceAssignment):
            # e.g. sentence_0 => sentence_2
            return clause.input_tuple, clause.output_tuple

        elif isinstance(clause, HornClauseForTask):
            # e.g. topic_0 => sentence_0
            return clause.input_tuple, clause.output_tuple

        else:
            raise ValueError(f"Unknown clause type {type(clause)} in query plan.")

    def get_task_from_clause(self, clause: HornClause) -> Task:
        """
        Get the task from a clause.
        Args:
            clause (HornClause): The clause to get the task from
        Returns:
            Task: The task from the clause
        """
        if isinstance(clause, HornClauseForDepedendentDescriptor):
            return clause.dependent_task.task

        elif isinstance(clause, HornClauseForTask):
            return clause.task

        else:
            raise ValueError(f"Unknown clause type {type(clause)} in query plan.")

    def get_resource(
        self, resource_tuple: tuple[type[BaseResource], int]
    ) -> BaseResource:
        """
        Get a resource from the resource values.
        Args:
            resource_tuple (tuple[type[BaseResource], int]): The resource tuple to get
        Returns:
            BaseResource: The resource from the resource values
        """
        if resource_tuple not in self.resource_values:
            raise ValueError(f"Resource {resource_tuple} not found in resource values.")

        return self.resource_values[resource_tuple]

    def update_plan(self, new_plan: QueryPlan, step: int) -> None:
        """
        Update the query plan and step.
        Args:
            new_plan (QueryPlan): The new query plan
            step (int): The step in the new query plan
        """
        self.query_plan = new_plan
        self.step = step

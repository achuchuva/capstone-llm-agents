"""Communication protocol for the MAS."""

from mas.ag2.ag2_task import AG2Task
from mas.agent import MASAgent
from mas.base_resource import BaseResource
from mas.communication.checkpoint import Checkpoint
from mas.communication.communication_interface import CommunicationInterface
from mas.communication.message import Message
from mas.query.query_plan import QueryPlan
from mas.task import Task


class CommunicationProtocol:
    """Communication protocol for the MAS."""

    checkpoints: list[Checkpoint]
    """List of checkpoints in the communication protocol."""

    agent_to_interface: dict[MASAgent, CommunicationInterface]
    """Dictionary of agents to their communication interfaces."""

    def __init__(self):
        """
        Initialise the communication protocol.
        """
        self.checkpoints = []
        self.agent_to_interface = {}

        self.checkpoint_index = 0
        """Index of the current checkpoint in the communication protocol."""

        self.max_retries = 10
        """Maximum number of retries for the communication protocol."""

        self.retries = 0
        """Number of retries for the communication protocol."""

    def reset(self):
        """Reset the communication protocol."""
        self.checkpoint_index = 0
        self.retries = 0

    def could_not_satisfy_query(self) -> bool:
        """Check if the communication protocol has failed to satisfy the query.

        Returns:
            bool: True if the communication protocol has failed, False otherwise.
        """
        # TODO check if we have failed at the checkpoint n times rather than total across all checkpoints
        return self.retries >= self.max_retries

    def add_checkpoint(self, checkpoint: Checkpoint):
        """Add a checkpoint to the communication protocol.

        Args:
            checkpoint (Checkpoint): The checkpoint to be added to the communication protocol.
        """
        self.checkpoints.append(checkpoint)

    def add_agent_interface(self, agent: MASAgent, interface: CommunicationInterface):
        """Add an agent and its communication interface to the communication protocol.

        Args:
            agent (MASAgent): The agent to be added to the communication protocol.
            interface (CommunicationInterface): The communication interface of the agent.
        """
        self.agent_to_interface[agent] = interface

    def get_agent_interface(self, agent: MASAgent) -> CommunicationInterface | None:
        """Get the communication interface of the agent.

        Args:
            agent (MASAgent): The agent to get the communication interface for.
        Returns:
            CommunicationInterface | None: The communication interface of the agent, or None if it does not exist.
        """
        return self.agent_to_interface.get(agent, None)

    def wrap(self, task: Task, input_resource: BaseResource) -> Message:
        """Wrap the task and its input resource in a message.

        Args:
            task (Task): The task to be wrapped in a message.
            input_resource (BaseResource): The input resource for the task.
        Returns:
            Message: The message that the clause is wrapped in.
        """
        # TODO abstract task and input into a new class

        # TODO get agent sender and recipient
        # unknown agent
        unknown_agent = MASAgent(
            name="unknown",
            description="unknown",
        )

        recipient = unknown_agent

        # TODO refactor Task:
        # Task, AgentTask which inherits from Task, and AG2Task which inherits from AgentTask

        # TODO temp
        if isinstance(task, AG2Task):
            recipient = task.agent

        message = Message(
            resource=input_resource,
            expected_resource_type=type(input_resource),
            recipient=recipient,
            sender=unknown_agent,
            metadata=[],
        )

        return message

    def handle_message(self, message: Message) -> Message:
        """Handle the message through the communication protocol.

        Args:
            message (Message): The message to be handled.
        Returns:
            Message: The new message after it has been handled.
        """
        # get recipient agent
        recipient = message.recipient

        # get interface
        interface = self.get_agent_interface(recipient)

        print(f"Handling message: {message}")
        print(f"Recipient: {recipient}")

        # all interfaces
        print(f"All interfaces: {self.agent_to_interface}")

        print(f"Interface: {interface}")

        # has no interface, assume that message can processed automatically
        if interface is None:
            return message

        return interface.handle_message(message)

    def alter_plan(
        self, plan: QueryPlan, step: int, message: Message
    ) -> tuple[QueryPlan, int]:
        """Alter the plan based on the message.

        Args:
            plan (QueryPlan): The plan to be altered.
            step (int): The current step in the plan.
            message (Message): The message to be handled.
        Returns:
            tuple[QueryPlan, int]: The new plan and the index of where to resume the plan.
        """

        # NOTE: If the solution is to retry, it will already be handled
        # because the plan naturally resumes at the same step

        # NOTE: But if the solution is to change the actual message sent then we need to update the plan

        # TODO solutions should update the plan
        # unless the checkpoint wants to raise an error upstream (e.g. to the previous checkpoint)
        # this means that all agents after the checkpoint do not know what to do
        # because we don't want to go back to the previous checkpoint (maybe later we can support this)
        # so we should say that the query cannot be satisfied

        # increment retries
        self.retries += 1

        return plan, step

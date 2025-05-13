import random

from core.agent import Agent
from core.chat import ChatHistory, Query
from core.communication_protocol import CommunicationProtocol
from core.entity import Entity


class CommunicationProtocolSpoof(CommunicationProtocol):
    """A spoof for the Communication Protocol."""

    # TODO: supported by Sprint 3

    def create_query(self, chat_history: ChatHistory, agents: list[Agent]) -> Query:
        """Create a new query from the chat history."""

        if len(agents) == 0:
            raise ValueError("No agents in the MAS. There must be at least one agent.")

        if self.history_appears_complete(chat_history):
            return self.continue_conversation_query()

        # last message
        last_message = chat_history.get_last_message()

        if last_message is None:
            # NOTE: Assumes that there is no chat, so the MAS should prompt the user
            return Query(self.user, "Hello, how can I help you?")

        # make copy of agents as a set
        entities: set[Entity] = set()
        for agent in agents:
            entities.add(agent)

        # add user to entities
        entities.add(self.user)

        # remove self
        entities.discard(last_message.who)

        entity_list = list(entities)

        # pick random entity
        entity = random.choice(entity_list)

        # create a query from the last message
        return Query(entity, f"{last_message.content}")

    def continue_conversation_query(self) -> Query:
        """Continue the conversation with a query."""

        # create a query from the last message
        return Query(self.user, "Is there anything else I can help you with?")

    def history_appears_complete(self, chat_history: ChatHistory) -> bool:
        """Check if the chat history appears complete."""
        return False

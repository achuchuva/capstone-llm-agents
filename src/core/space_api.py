from core.chat import ChatHistory
from core.mas import MAS
from core.space import Space


class SpaceAPI:
    """API layer for accessing the differente spaces in the MAS."""

    def __init__(self, spaces: list[Space], mas: MAS):
        self.spaces = spaces
        self.mas = mas

    def get_spaces(self) -> list[Space]:
        """Get all spaces in the MAS."""
        return self.spaces

    def get_chat_history_for_space(self, space: Space) -> ChatHistory:
        """Get the chat history for a specific space."""
        return space.get_chat_history()

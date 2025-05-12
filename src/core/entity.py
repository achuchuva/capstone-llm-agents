class Entity:
    """An entity in a conversation."""

    def __init__(self, name: str, description: str, role: str):
        self.name = name
        self.description = description
        self.role = role


class HumanUser(Entity):
    """A human user in a conversation."""

    def __init__(self, name: str, description: str):
        super().__init__(name, description, "user")

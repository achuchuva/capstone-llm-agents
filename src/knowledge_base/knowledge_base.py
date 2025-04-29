"""Knowledge Base for storing and retrieving information utilising pydantic's BaseModel."""

import json
from pydantic import BaseModel
from typing import Dict


class KnowledgeBase:
    def __init__(self):
        self._kb_model = BaseModel()

    def add(self, key: str, value: str):
        self._kb_model.data[key.lower()] = value.strip()

    def remove(self, key: str):
        self._kb_model.data.pop(key.lower(), None)

    def get(self, key: str) -> str | None:
        return self._kb_model.data.get(key.lower())

    def contains(self, key: str) -> bool:
        return key.lower() in self._kb_model.data

    def to_dict(self) -> Dict[str, str]:
        return self._kb_model.data.copy()

    def to_json(self, indent=2) -> str:
        return self._kb_model.json(indent=indent)

    def to_bullet_string(self) -> str:
        return "\n".join(
            f"- {k.capitalize()}: {v}" for k, v in self._kb_model.data.items()
        )

    @property
    def model(self) -> BaseModel:
        """Expose underlying Pydantic model (read-only)."""
        return self._kb_model

from autogen import ConversableAgent
from app import App
from capabilities.knowledge_base import (
    BasicChunker,
    MultipleKnowledgeBase,
    SelectAllKnowledgeBaseSelector,
)
from core.capability import Capability
from extractor import DEFAULT_EXTRACTOR
from implementations.faiss_kb import FAISSKnowledgeBase


default_capabilities: list[Capability] = []
app = App(default_capabilities)

# Capabilities
# ============

# add kb

# NOTE: the token count in BasicChunker does not do anything meaningful atm
# because it gets ignored in the FAISSKnowledgeBase
faiss_kb = FAISSKnowledgeBase(BasicChunker(1000), DEFAULT_EXTRACTOR, 3, 1000)

multi_kb = MultipleKnowledgeBase(
    faiss_kb,
    SelectAllKnowledgeBaseSelector(),
)

default_capabilities.append(multi_kb)

# Agents
# ======

# add agent
app.add_ag2_agent(
    ConversableAgent(
        name="Assistant",
        system_message="You are a helpful assistant.",
        llm_config={"api_type": "ollama", "model": "gemma3"},
    ),
    default_capabilities,
)

app.run()

from autogen import ConversableAgent
from app import App
from capabilities.knowledge_base import (
    BasicChunker,
    FolderKB,
    SelectAllKnowledgeBaseSelector,
)
from core.capability import Capability
from extractor import DEFAULT_EXTRACTOR
from implementations.faiss_kb import FAISSKnowledgeBase


default_capabilities: list[Capability] = []

# Capabilities
# ============

# add kb

# NOTE: the token count in BasicChunker does not do anything meaningful atm
# because it gets ignored in the FAISSKnowledgeBase
faiss_kb = FAISSKnowledgeBase(BasicChunker(1000), DEFAULT_EXTRACTOR)

# multi_kb = MultipleKnowledgeBase(
#     faiss_kb,
#     SelectAllKnowledgeBaseSelector(),
# )

folder_kb = FolderKB("./kb", faiss_kb, SelectAllKnowledgeBaseSelector())

default_capabilities.append(folder_kb)

# Build App
# =========
app = App(default_capabilities, folder_kb)

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

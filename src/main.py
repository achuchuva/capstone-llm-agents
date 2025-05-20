from autogen import ConversableAgent
import fitz
from app import App
from capabilities.knowledge_base import (
    BasicChunker,
    DocumentReader,
    LocalDocumentKnowledgeExtractor,
    MultipleDocumentReader,
)
from core.capability import Capability
from implementations.faiss_kb import FAISSKnowledgeBase


default_capabilities: list[Capability] = []
app = App(default_capabilities)

# Capabilities
# ============

# add kb


class TextReader(DocumentReader):
    """A simple text reader to extract text from text files."""

    def __init__(self):
        supported_extensions = [".txt"]
        super().__init__(supported_extensions)

    def read(self, path: str, extension: str) -> str:
        """Read a document from a path."""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


class PDFReader(DocumentReader):
    """A simple PDF reader to extract text from PDF files."""

    def __init__(self):
        supported_extensions = [".pdf"]
        super().__init__(supported_extensions)

    def read(self, path: str, extension: str) -> str:
        """Read a document from a path."""

        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text


reader = MultipleDocumentReader(
    [
        PDFReader(),
        TextReader(),
    ]
)

default_capabilities.append(
    FAISSKnowledgeBase(
        BasicChunker(100), LocalDocumentKnowledgeExtractor(reader), 3, 1000
    )
)

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

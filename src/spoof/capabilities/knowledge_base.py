from capabilities.knowledge_base import (
    BasicChunker,
    Document,
    DocumentReader,
    Knowledge,
    KnowledgeBase,
    LocalDocumentKnowledgeExtractor,
)


class DocumentSpoof(Document):
    """A spoof for the Document class."""

    def to_text(self) -> str:
        """Convert the document to text."""

        # assume that the document is a txt
        if not self.extension == "txt":
            raise ValueError(f"Unsupported file extension: {self.extension}")

        # read lines
        with open(self.path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            text = "".join(lines)
        return text

    @staticmethod
    def get_file_extension(path: str) -> str:
        """Get the file extension."""
        return "txt"

    @staticmethod
    def get_last_modified_time(path: str) -> str:
        """Get the last modified time."""
        return "2023-10-01T00:00:00Z"


class ReaderSpoof(DocumentReader):
    """A spoof for the DocumentReader class."""

    def read(self, path: str, extension: str) -> str:
        """Read the document."""
        return " ".join(["This is a spoofed document."] * 3)

    def get_file_extension(self) -> str:
        """Get the file extension."""
        return "txt"

    def get_last_modified_time(self, _: str) -> str:
        """Get the last modified time."""
        return "2023-10-01T00:00:00Z"


class KnowledgeBaseSpoof(KnowledgeBase):
    """A spoof for the KnowledgeBase capability."""

    knowledge_base: list[Knowledge]

    def __init__(self):
        super().__init__(
            BasicChunker(100), LocalDocumentKnowledgeExtractor(ReaderSpoof)
        )
        self.knowledge_base = []

        self.chunk_size = 128

    def ingest_chunks(self, chunks: list[Knowledge]) -> None:
        """Ingest chunks into the knowledge base."""
        # for simplicity, we will just append the chunks to the knowledge base.
        self.knowledge_base.extend(chunks)

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """Retrieve knowledge related to a query."""
        # for simplicity, we will just return the first 5 knowledge items.
        return self.knowledge_base[:5]

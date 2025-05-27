import os
from core.capability import Capability


class Knowledge:
    """A simple knowledge representation to store information."""

    def __init__(self, knowledge: str):
        self.knowledge = knowledge

    def __str__(self) -> str:
        return self.knowledge


class Document:
    """A document to be ingested into the knowledge base that could be a PDF, Word document, etc. provided by the user."""

    def __init__(self, path: str, extension: str):
        self.path = path
        self.extension = extension

    def to_text(self) -> str:
        """Convert the document to text."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class Folder:
    """A folder containing documents to be ingested into the knowledge base, including subfolders."""

    def __init__(self, path: str):
        self.path = path

    def get_documents(self) -> list[Document]:
        """Get all files in the folder and subfolders as Document instances."""
        print(f"Getting documents from folder (recursively): {self.path}")
        if not os.path.isdir(self.path):
            raise ValueError(f"Invalid directory path: {self.path}")

        documents = []
        for dirpath, _, filenames in os.walk(self.path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                _, ext = os.path.splitext(filename)
                ext = ext.lstrip(".").lower()
                documents.append(Document(path=full_path, extension=ext))
        return documents


class KnowledgeBase(Capability):
    """A simple knowledge base to store and retrieve information that the agent can use."""

    def __init__(self, supported_extensions: list[str]):
        super().__init__("knowledge_base")
        self.supported_extensions = supported_extensions

    def add_knowledge(self, knowledge: Knowledge):
        """Add knowledge to the knowledge base."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def is_supported_extension(self, extension: str) -> bool:
        """Check if the extension is supported."""
        return extension in self.supported_extensions

    def ingest_document(self, document: Document) -> bool:
        """
        Ingest a document into the knowledge base.
        Returns True if document was successfully ingested, False otherwise.
        """
        if not self.is_supported_extension(document.extension):
            raise ValueError(f"Unsupported file extension: {document.extension}")

        text = document.to_text()
        knowledge = self.chunk_text_to_knowledge(text)

        for k in knowledge:
            self.add_knowledge(k)

    def ingest_folder(self, folder: Folder):
        """Ingests all supported documents in a given folder."""
        documents = folder.get_documents()

        for document in documents:
            try:
                self.ingest_document(document)
            except Exception as e:
                print(f"Failed to ingest {document.path}: {e}")

    def chunk_text_to_knowledge(self, text: str) -> list[Knowledge]:
        """Chunk text into knowledge."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """Retrieve knowledge related to a query."""
        raise NotImplementedError("This method should be implemented by subclasses.")

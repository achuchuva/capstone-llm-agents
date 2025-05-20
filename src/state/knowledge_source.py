"""Module for knowledge source management."""

from capabilities.knowledge_base import Document


class KnowledgeSource:
    """A knowledge source is a collection of documents that agents can have access to."""

    documents: list[Document]

    def __init__(self, name: str):
        self.name = name
        self.documents = []

    def add_document(self, document: Document):
        """Add a document to the knowledge source."""
        self.documents.append(document)

    def get_documents(self) -> list[Document]:
        """Get the documents in the knowledge source."""
        return self.documents

    def update_source(self):
        """Update the knowledge source, refreshing the documents."""
        raise NotImplementedError("This method should be implemented in subclasses.")


class FolderKnowledgeSource(KnowledgeSource):
    """A knowledge source loads documents from a folder."""

    def __init__(self, name: str, folder_path: str):
        super().__init__(name)
        self.folder_path = folder_path

    def update_source(self):
        """Update the knowledge source by refreshing the documents from the folder."""
        # check if any new documents have been added to the folder

        # if so, add them to the documents list

        # check if any documents have been updated

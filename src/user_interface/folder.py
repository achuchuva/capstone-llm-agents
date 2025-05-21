import os
from capabilities.knowledge_base import FolderKB, LocalDocument


class FolderAPI:
    """Folder API to manage the documents in a folder."""

    def __init__(self, folder_path: str, kb: FolderKB):
        self.folder_path = folder_path
        self.kb = kb

    def update(self):
        """Update the documents in the knowledge base based on the documents in the actual file system folder."""
        documents_from_fs = self.get_documents_in_fs()
        documents_from_kb = self.get_documents_in_kb()

        # get the changes
        added_docs, edited_docs, removed_docs = self.get_changes(
            documents_from_fs, documents_from_kb
        )

        # handle the changes
        for doc in added_docs:
            self.kb.add_document(doc)
        for doc in edited_docs:
            self.kb.update_document(doc)
        for doc in removed_docs:
            self.kb.remove_document(doc)

    def get_documents_in_kb(self) -> list[LocalDocument]:
        """Get all the documents in the kb."""
        return self.kb.get_documents()

    def get_documents_in_fs(self) -> list[LocalDocument]:
        """Get all the documents in the folder in the file system."""
        documents: list[LocalDocument] = []

        for root, _, files in os.walk(self.folder_path):
            for file in files:
                path = os.path.join(root, file)

                # create a document object
                doc = LocalDocument(path)
                documents.append(doc)

        return documents

    def get_changes(
        self,
        documents_from_fs: list[LocalDocument],
        documents_from_kb: list[LocalDocument],
    ) -> tuple[list[LocalDocument], list[LocalDocument], list[LocalDocument]]:
        """Gets the changes from the last version of the folder. Returns the added, edited, and removed documents."""

        doc_paths_in_kb = set(doc.path for doc in documents_from_kb)
        doc_paths_in_fs = set(doc.path for doc in documents_from_fs)

        lookup = {doc.path: doc for doc in documents_from_kb}

        added_docs: list[LocalDocument] = []
        edited_docs: list[LocalDocument] = []
        removed_docs: list[LocalDocument] = []

        for doc_from_fs in documents_from_fs:
            # new document
            if doc_from_fs.path not in doc_paths_in_kb:

                # log the change
                added_docs.append(doc_from_fs)
                continue

            # document has been modified
            original_doc = lookup.get(doc_from_fs.path)
            new_doc = doc_from_fs

            if self.document_has_been_modified(original_doc, new_doc):
                # update the document time
                original_doc.last_modified_time = new_doc.last_modified_time

                # log the change
                edited_docs.append(original_doc)

        # check for removed documents
        for doc_from_kb in documents_from_kb:
            if doc_from_kb.path not in doc_paths_in_fs:
                # log the change
                removed_docs.append(doc_from_kb)

        return added_docs, edited_docs, removed_docs

    def document_has_been_modified(
        self, original_doc: LocalDocument, new_doc: LocalDocument
    ) -> bool:
        """Check if the document has been modified."""
        if (
            original_doc.last_modified_time is None
            or new_doc.last_modified_time is None
        ):
            return False
        return original_doc.last_modified_time != new_doc.last_modified_time

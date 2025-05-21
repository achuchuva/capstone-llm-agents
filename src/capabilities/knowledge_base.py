import os

from core.capability import Capability


class Knowledge:
    """A simple knowledge representation to store information."""

    def __init__(self, knowledge: str, source: "KnowledgeSource"):
        self.knowledge = knowledge
        self.source = source

    def __str__(self) -> str:
        return self.knowledge


class KnowledgeSource:
    """A knowledge source yields some knowledge."""


class KnowledgeExtractor:
    """A knowledge extractor is a class that extracts knowledge from a source."""

    def __init__(self, supported_sources: list[type[KnowledgeSource]]):
        self.supported_sources = supported_sources

    def is_supported_source(self, source: KnowledgeSource) -> bool:
        """Check if the source is supported."""
        return isinstance(source, tuple(self.supported_sources))

    def safe_extract(self, knowledge_source: KnowledgeSource) -> list[Knowledge]:
        """Safely extract knowledge from the source."""
        if not self.is_supported_source(knowledge_source):
            raise ValueError(f"Unsupported knowledge source: {type(knowledge_source)}")

        return self.extract(knowledge_source)

    def extract(self, knowledge_source: KnowledgeSource) -> list[Knowledge]:
        """Extract knowledge from the source."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class DefaultMultipleKnowledgeExtractor(KnowledgeExtractor):
    """A default knowledge extractor that extracts knowledge from multiple sources."""

    def __init__(self, extractor: KnowledgeExtractor):
        super().__init__(extractor.supported_sources)
        self.extractor = extractor

    def extract(self, knowledge_source: KnowledgeSource) -> list[Knowledge]:
        """Extract knowledge from the source."""
        if not isinstance(knowledge_source, MultipleKnowledgeSource):
            raise ValueError("Knowledge source is not a multiple knowledge source.")

        knowledge: list[Knowledge] = []
        for ks in knowledge_source.knowledge_sources:
            knowledge.extend(self.extractor.safe_extract(ks))

        return knowledge


class SmartKnowledgeExtractor(KnowledgeExtractor):
    """A smart knowledge extractor that extracts knowledge from multiple sources."""

    def __init__(self, supported_sources: list[type[KnowledgeSource]]):
        supported_sources = supported_sources + [MultipleKnowledgeSource]
        super().__init__(supported_sources)

    def extract(self, knowledge_source: KnowledgeSource) -> list[Knowledge]:
        """Extract knowledge from the source."""
        if isinstance(knowledge_source, MultipleKnowledgeSource):
            return DefaultMultipleKnowledgeExtractor(self).extract(knowledge_source)

        return self.safe_extract(knowledge_source)


class MultipleKnowledgeSource(KnowledgeSource):
    """A knowledge source that yields multiple knowledge sources."""

    knowledge_sources: list[KnowledgeSource]

    def __init__(self, name: str, extractor: KnowledgeExtractor):
        self.name = name
        self.knowledge_sources = []
        self.extractor = extractor

    def add_knowledge_source(self, knowledge_source: KnowledgeSource):
        """Add a knowledge source to the list."""
        self.knowledge_sources.append(knowledge_source)


class Document(KnowledgeSource):
    """A document is a knowledge source that has some text."""

    def __init__(
        self, path: str, extension: str, last_modified_time: float | None = None
    ):
        self.path = path
        self.extension = extension
        self.last_modified_time = last_modified_time

    @staticmethod
    def get_file_extension(path: str) -> str:
        """Get the file extension of a document."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @staticmethod
    def get_last_modified_time(path: str) -> float:
        """Get the last modified time of a document."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class LocalDocument(Document):
    """A document accessible from a path to a local file."""

    def __init__(self, path: str):
        super().__init__(path, self.get_file_extension(path))
        self.last_modified_time = self.get_last_modified_time(path)

    @staticmethod
    def get_file_extension(path: str) -> str:
        """Get the file extension of a document."""
        return os.path.splitext(path)[1]

    @staticmethod
    def get_last_modified_time(path: str) -> float:
        """Get the last modified time of a document."""
        try:
            return os.path.getmtime(path)

        # TODO: handling here is not ideal, but it is a good start
        except (FileNotFoundError, OSError, PermissionError):
            return None

    def __hash__(self):
        return hash(f"{self.path}{self.last_modified_time}")

    def __str__(self):
        return f"Document(path={self.path}, extension={self.extension}, last_modified_time={self.last_modified_time})"

    def __eq__(self, other):
        if not isinstance(other, LocalDocument):
            return False

        return (
            self.path == other.path
            and self.extension == other.extension
            and self.last_modified_time == other.last_modified_time
        )


class DocumentReader:
    """A document reader is a class that reads documents from a path."""

    def __init__(self, supported_extensions: list[str]):
        self.supported_extensions = supported_extensions

    def is_supported_extension(self, extension: str) -> bool:
        """Check if the extension is supported."""
        return extension in self.supported_extensions

    def safe_read(self, path: str, extension: str) -> str:
        """Safely read a document from a path."""

        if not self.is_supported_extension(extension):
            raise ValueError(f"Unsupported file extension: {extension}")

        return self.read(path, extension)

    def read(self, path: str, extension: str) -> str:
        """Read a document from a path."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class MultipleDocumentReader(DocumentReader):
    """A document reader that delegates to multiple readers."""

    reader_map: dict[str, DocumentReader]

    def __init__(self, readers: list[DocumentReader]):
        all_supported_extensions = set()

        for reader in readers:
            all_supported_extensions.update(reader.supported_extensions)

        super().__init__(list(all_supported_extensions))
        self.readers = readers

        self.reader_map = {}

        for reader in readers:
            for ext in reader.supported_extensions:

                if ext in self.reader_map:
                    raise ValueError(
                        f"Extension {ext} is already supported by another reader."
                    )

                self.reader_map[ext] = reader

    def add_reader(self, reader: DocumentReader):
        """Add a reader to the list of readers."""
        self.readers.append(reader)

        # update the supported extensions
        self.supported_extensions.extend(reader.supported_extensions)

        # update the reader map
        for ext in reader.supported_extensions:
            self.reader_map[ext] = reader

    def read(self, path: str, extension: str) -> str:
        """Read a document from a path."""

        # find the reader for the extension
        reader = self.reader_map.get(extension)

        return reader.read(path, extension)


class LocalDocumentKnowledgeExtractor(SmartKnowledgeExtractor):
    """Extracts knowledge from local documents."""

    def __init__(self, reader: DocumentReader):
        supported_sources = [LocalDocument]
        super().__init__(supported_sources)
        self.reader = reader

    def extract(self, knowledge_source: KnowledgeSource) -> list[Knowledge]:
        """Extract knowledge from the source."""

        assert isinstance(knowledge_source, LocalDocument)

        # read the document
        text = self.reader.safe_read(knowledge_source.path, knowledge_source.extension)

        # create a knowledge object
        knowledge = Knowledge(text, knowledge_source)

        return [knowledge]


class KnowledgeChunker:
    """A knowledge chunker is a class that chunks knowledge sources into smaller pieces."""

    def chunk(
        self, knowledge_source: KnowledgeSource, extractor: KnowledgeExtractor
    ) -> list[Knowledge]:
        """Chunk the knowledge source into smaller pieces."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    @staticmethod
    def group_chunks_by_source(
        chunks: list[Knowledge],
    ) -> dict[KnowledgeSource, list[Knowledge]]:
        """Group chunks by their source."""
        grouped_chunks: dict[KnowledgeSource, list[Knowledge]] = {}

        for chunk in chunks:
            if chunk.source not in grouped_chunks:
                grouped_chunks[chunk.source] = []

            grouped_chunks[chunk.source].append(chunk)

        return grouped_chunks


class BasicChunker(KnowledgeChunker):
    """A basic chunker that just returns combines all the knowledge and chunks it to some size."""

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def chunk(
        self, knowledge_source: KnowledgeSource, extractor: KnowledgeExtractor
    ) -> list[Knowledge]:
        """Chunk the knowledge source into smaller pieces."""

        knowledge = extractor.safe_extract(knowledge_source)

        grouped_chunks = KnowledgeChunker.group_chunks_by_source(knowledge)

        chunks: list[Knowledge] = []
        for source, source_chunks in grouped_chunks.items():

            # combine all the knowledge into a single string
            combined_knowledge = " ".join([str(chunk) for chunk in source_chunks])

            # chunk the knowledge into smaller pieces
            for i in range(0, len(combined_knowledge), self.chunk_size):
                start = i
                end = i + self.chunk_size
                chunk_text = combined_knowledge[start:end]
                chunks.append(Knowledge(chunk_text, source))

        return chunks


class KnowledgeBase(Capability):
    """A simple knowledge base to store and retrieve information that the agent can use."""

    def __init__(self, chunker: KnowledgeChunker, extractor: KnowledgeExtractor):
        super().__init__("knowledge_base")
        self.chunker = chunker
        self.extractor = extractor

    def ingest_knowledge_source(self, knowledge_source: KnowledgeSource):
        """Ingest a knowledge source into the knowledge base."""
        chunks = self.chunk_knowledge_source(knowledge_source)
        self.ingest_chunks(chunks)

    def chunk_knowledge_source(
        self, knowledge_source: KnowledgeSource
    ) -> list[Knowledge]:
        """Chunk the knowledge source into smaller pieces."""
        return self.chunker.chunk(knowledge_source, self.extractor)

    def ingest_chunks(self, chunks: list[Knowledge]):
        """Ingest chunks into the knowledge base."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """Retrieve knowledge related to a query."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def copy(self) -> "KnowledgeBase":
        """Create a copy of the knowledge base."""
        # TODO assumes that the extractor and chunker are stateless
        raise NotImplementedError("This method should be implemented by subclasses. ")

    def reset(self):
        """Reset the knowledge base."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class KnowledgeBaseSelector:
    """Gets the relevant knowledge bases for a query."""

    def get_relevant_knowledge_bases(
        self, query: str, knowledge_bases: list[KnowledgeBase]
    ) -> list[KnowledgeBase]:
        """Get the relevant knowledge bases for a query."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SelectAllKnowledgeBaseSelector(KnowledgeBaseSelector):
    """A knowledge base selector that selects all knowledge bases."""

    def get_relevant_knowledge_bases(
        self, query: str, knowledge_bases: list[KnowledgeBase]
    ) -> list[KnowledgeBase]:
        """Get the relevant knowledge bases for a query."""
        return knowledge_bases


# TODO: make the folder generic in case you have a remote folder but who asked
class LocalFolderKnowledgeSource(KnowledgeSource):
    """A folder of many diffent documents."""

    documents: list[LocalDocument]

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.documents = []

    def add_document(self, document: LocalDocument):
        """Add a document to the folder."""
        self.documents.append(document)

    def get_documents(self) -> list[LocalDocument]:
        """Get the documents in the folder."""
        return self.documents

    def remove_document(self, document: LocalDocument):
        """Remove a document from the folder."""
        self.documents.remove(document)

    def edit_document(self, document: LocalDocument):
        """Edit a document in the folder."""

        # get matching document
        for doc in self.documents:
            if doc.path == document.path:
                # remove the old document
                self.documents.remove(doc)

        # add the new document
        self.documents.append(document)


class MultipleKnowledgeBase(KnowledgeBase):
    """A knowledge base that splits each knowledge source into its own knowledge base."""

    knowledge_bases: list[KnowledgeBase]
    knowledge_sources: set[KnowledgeSource]

    # map from knowledge base to source
    knowledge_source_map: dict[KnowledgeBase, KnowledgeSource]

    def __init__(
        self,
        base_knowledge_base: KnowledgeBase,
        knowledge_base_selector: KnowledgeBaseSelector,
    ):
        self.base_knowledge_base = base_knowledge_base
        chunker = base_knowledge_base.chunker
        extractor = base_knowledge_base.extractor
        super().__init__(chunker, extractor)
        self.knowledge_bases = []
        self.knowledge_sources = set()
        self.knowledge_source_map = {}
        self.knowledge_base_selector = knowledge_base_selector

    def ingest_chunks(self, chunks: list[Knowledge]):
        """Ingest chunks into the knowledge base."""

        for chunk in chunks:
            # check if the source is already in the knowledge base
            if chunk.source not in self.knowledge_sources:

                # if not, create a new knowledge base for the source
                kb = self.base_knowledge_base.copy()

                # add the new knowledge base to system
                self.knowledge_bases.append(kb)
                self.knowledge_sources.add(chunk.source)
                self.knowledge_source_map[kb] = chunk.source

        # group by source
        grouped_chunks = KnowledgeChunker.group_chunks_by_source(chunks)

        for kb in self.knowledge_bases:
            # get the source of the knowledge base
            source = self.knowledge_source_map[kb]

            # get the chunks for the source
            kb_chunks = grouped_chunks.get(source, [])

            # ingest the chunks into the knowledge base
            kb.ingest_chunks(kb_chunks)

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """Retrieve knowledge related to a query."""
        relevant_kbs = self.get_relevant_knowledge_bases(query)

        knowledge: list[Knowledge] = []
        for kb in relevant_kbs:
            knowledge.extend(kb.retrieve_related_knowledge(query))

        return knowledge

    def get_relevant_knowledge_bases(self, query: str) -> list[KnowledgeBase]:
        """Get the relevant knowledge bases for a query."""
        return self.knowledge_base_selector.get_relevant_knowledge_bases(
            query, self.knowledge_bases
        )

    def copy(self) -> "KnowledgeBase":
        """Create a copy of the knowledge base."""
        return MultipleKnowledgeBase(
            self.base_knowledge_base.copy(), self.knowledge_base_selector
        )

    def remove_source(self, source: KnowledgeSource):
        """Remove a source from the knowledge base."""

        # flip the map to get the knowledge base from the source
        knowledge_source_map = MultipleKnowledgeBase.flip_map(self.knowledge_source_map)

        # remove the source from the map
        kb = knowledge_source_map.get(source)

        if kb is None:
            raise ValueError(f"Source not found in knowledge base: {source}")

        # remove the knowledge base
        self.knowledge_bases.remove(kb)
        self.knowledge_sources.remove(source)

        # delete the kb and source from the map
        del self.knowledge_source_map[kb]

        print("Removed source:", source)
        print("Removed kb:", kb)
        print("Knowledge bases:", self.knowledge_bases)
        print("Knowledge sources:", self.knowledge_sources)
        print("Knowledge source map:", self.knowledge_source_map)

    def reset(self):
        """Reset the knowledge base."""
        for kb in self.knowledge_bases:
            kb.reset()

        # TODO not sure if it should also remove the sources

    def remove_all_sources(self):
        """Remove all sources from the knowledge base."""
        self.knowledge_bases = []
        self.knowledge_sources = set()
        self.knowledge_source_map = {}

    @staticmethod
    def flip_map(
        knowledge_source_map: dict[KnowledgeBase, KnowledgeSource],
    ) -> dict[KnowledgeSource, KnowledgeBase]:
        """Flip the map from knowledge base to source to source to knowledge base."""
        flipped_map: dict[KnowledgeSource, KnowledgeBase] = {}

        for kb, source in knowledge_source_map.items():
            flipped_map[source] = kb

        return flipped_map


class FolderKB(MultipleKnowledgeBase):
    """A knowledge base that is a folder of many different documents."""

    def __init__(
        self,
        folder_path: str,
        base_knowledge_base: KnowledgeBase,
        selector: KnowledgeBaseSelector,
    ):
        super().__init__(
            base_knowledge_base,
            selector,
        )
        self.folder_path = folder_path
        self.folder_source = LocalFolderKnowledgeSource(folder_path)

    def get_documents(self) -> list[LocalDocument]:
        """Get the documents in the folder."""
        return self.folder_source.get_documents()

    def add_document(self, document: LocalDocument):
        """Add a document to the folder."""
        self.folder_source.add_document(document)
        self.ingest_knowledge_source(document)

    def remove_document(self, document: LocalDocument):
        """Remove a document from the folder."""

        # flip the map to get the source from the knowledge base
        knowledge_kb_map = MultipleKnowledgeBase.flip_map(self.knowledge_source_map)

        kb = knowledge_kb_map.get(document)

        print("Kb to remove doc from:", kb)
        print("Document to remove:", document)

        if kb is None:
            raise ValueError(f"Document not found in kb: {document.path}")

        # remove the source
        self.folder_source.remove_document(document)

        self.remove_source(document)

        kb.reset()

    def update_document(self, document: LocalDocument):
        """Edit a document in the folder."""
        # flip the map to get the source from the knowledge base
        knowledge_kb_map = MultipleKnowledgeBase.flip_map(self.knowledge_source_map)

        # get doc kb from the source
        kb = knowledge_kb_map.get(document)

        if kb is None:
            raise ValueError(f"Document not found in folder: {document.path}")

        # edit
        self.folder_source.edit_document(document)

        kb.reset()

        self.ingest_knowledge_source(document)

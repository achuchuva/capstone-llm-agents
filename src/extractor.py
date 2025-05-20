import fitz
from capabilities.knowledge_base import (
    DocumentReader,
    LocalDocumentKnowledgeExtractor,
    MultipleDocumentReader,
)


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

DEFAULT_EXTRACTOR = LocalDocumentKnowledgeExtractor(reader)

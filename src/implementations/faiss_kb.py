from capabilities.knowledge_base import KnowledgeBase, Knowledge, Document
from sentence_transformers import SentenceTransformer
from transformers import GPT2TokenizerFast  # for token counting
import fitz, faiss, numpy as np


class FAISSKnowledgeBase(KnowledgeBase):
    """A knowledge base with per-document max_tokens and top_k support."""

    def __init__(
        self,
        supported_extensions: list[str],
        default_max_tokens: int = 100,
        default_top_k: int = 5,
    ):
        super().__init__("knowledge_base")
        self.supported_extensions = supported_extensions
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.documents = []  # Each document stores its own settings and index
        self.default_max_tokens = default_max_tokens
        self.default_top_k = default_top_k

    def is_supported_extension(self, extension: str) -> bool:
        return extension in self.supported_extensions

    def _estimate_document_heuristics(self, total_tokens: int) -> tuple[int, int]:
        """
        Heuristic that scales max_tokens and top_k based on document length.
        - For very small docs (~500 tokens): ~64, 3
        - For very large docs (~20000 tokens): ~1024, 9
        """

        # Scale max_tokens between 64 and 1024
        max_tokens = int(64 + (min(total_tokens, 20000) / 20000) * (1024 - 64))

        if total_tokens < 500:
            top_k = 3
        elif total_tokens < 2000:
            top_k = 4
        elif total_tokens < 5000:
            top_k = 5
        elif total_tokens < 10000:
            top_k = 4
        else:
            top_k = 3

        return max_tokens, top_k

    def ingest_document(self, document: Document):
        if not self.is_supported_extension(document.extension):
            raise ValueError(f"Unsupported file extension: {document.extension}")

        # Extract text
        texts = []
        if document.extension == "pdf":
            doc = fitz.open(document.path)
            for page in doc:
                texts.append(page.get_text())
        else:
            with open(document.path, "r", encoding="utf-8") as f:
                texts = [f.read()]

        full_text = "\n".join(texts)
        token_ids = self.tokenizer.encode(full_text)
        total_tokens = len(token_ids)

        # Apply heuristic to determine max_tokens and top_k
        max_tokens, top_k = self._estimate_document_heuristics(total_tokens)

        # Chunking
        all_chunks = []
        for i in range(0, total_tokens, max_tokens):
            chunk_ids = token_ids[i : i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_ids)
            all_chunks.append(chunk_text)

        if not all_chunks:
            return

        embeddings = self.model.encode(all_chunks)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings))

        self.documents.append(
            {
                "chunks": all_chunks,
                "embeddings": embeddings,
                "index": index,
                "max_tokens": max_tokens,
                "top_k": top_k,
                "length": total_tokens,
            }
        )

        print(
            f"Ingested document ({total_tokens} tokens) with {len(all_chunks)} chunks, "
            f"max_tokens={max_tokens}, top_k={top_k}."
        )

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """
        Retrieves top_k chunks most similar to the query.
        Embeds query and searches FAISS index:contentReference[oaicite:20]{index=20}.
        """
        if not self.documents:
            return []

        query_emb = self.model.encode([query])
        combined_results = []

        for doc in self.documents:
            D, I = doc["index"].search(np.array(query_emb), doc["top_k"])
            for dist, idx in zip(D[0], I[0]):
                if idx < len(doc["chunks"]):
                    combined_results.append((dist, doc["chunks"][idx]))

        combined_results.sort(key=lambda x: x[0])
        top_results = combined_results[: self.default_top_k]
        return [Knowledge(text) for _, text in top_results]

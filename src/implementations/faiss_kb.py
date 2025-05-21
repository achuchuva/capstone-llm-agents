from sentence_transformers import SentenceTransformer
from transformers import GPT2TokenizerFast  # for token counting
import faiss
import numpy as np

from capabilities.knowledge_base import (
    KnowledgeBase,
    Knowledge,
    KnowledgeChunker,
    KnowledgeExtractor,
)


class FAISSKnowledgeBase(KnowledgeBase):
    """A simple knowledge base to store and retrieve information that the agent can use."""

    def __init__(
        self,
        chunker: KnowledgeChunker,
        extractor: KnowledgeExtractor,
    ):
        super().__init__(chunker, extractor)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.embeddings = None  # will hold numpy array of embeddings
        self.index = None  # will hold FAISS index
        self.chunks = []  # will hold chunks of text

        self.top_k = None

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

    def ingest_chunks(self, chunks: list[Knowledge]):
        """Ingest chunks into the knowledge base."""

        texts = [text for chunk in chunks for text in chunk.knowledge]

        # combine all chunks into a single string
        combined_text = "".join(texts)

        # tokenise
        token_ids = self.tokenizer.encode(combined_text)

        # chunk
        all_chunks: list[str] = []

        # estimate heuristics
        total_tokens = len(token_ids)
        max_tokens, top_k = self._estimate_document_heuristics(total_tokens)

        for i in range(0, len(token_ids), max_tokens):
            start = i
            end = i + max_tokens
            chunk_ids = token_ids[start:end]
            chunk_text = self.tokenizer.decode(chunk_ids)
            all_chunks.append(chunk_text)

        if not all_chunks:
            return

        # encode and index chunks
        embeddings = self.model.encode(all_chunks)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings))

        self.index = index
        self.embeddings = embeddings
        self.chunks = all_chunks
        self.top_k = top_k

        # log
        print(f"Indexed {len(all_chunks)} chunks of text.")

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        """
        Retrieves top_k chunks most similar to the query.
        Embeds query and searches FAISS index:contentReference[oaicite:20]{index=20}.
        """

        # no saved embeddings
        if self.index is None:
            return []

        query_emb = self.model.encode([query])
        combined_results = []

        # TODO save source of knowledge
        source = None

        # get top_k
        top_k = self.top_k

        if top_k is None:
            raise ValueError("Top k is not set. Please ingest chunks first.")

        # Search each document index separately
        distance, index = self.index.search(np.array(query_emb), top_k)
        chunks = self.chunks
        for dist, idx in zip(distance[0], index[0]):

            # check if index is valid
            if idx < len(chunks):
                combined_results.append((dist, chunks[idx]))

        # sort all results by distance and return top_k overall
        combined_results.sort(key=lambda x: x[0])

        top_chunks = [Knowledge(text, source) for _, text in combined_results[:top_k]]

        return top_chunks

    def copy(self) -> "FAISSKnowledgeBase":
        """Create a copy of the knowledge base."""
        new_kb = FAISSKnowledgeBase(self.chunker, self.extractor)
        return new_kb

    def reset(self):
        """Reset the knowledge base."""
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.embeddings = None
        self.index = None
        self.chunks = []

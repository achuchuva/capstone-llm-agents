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
        top_k: int = 5,
        max_tokens: int = 100,
    ):
        super().__init__(chunker, extractor)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.embeddings = None  # will hold numpy array of embeddings
        self.index = None  # will hold FAISS index
        self.chunks = []  # will hold chunks of text
        self.top_k = top_k  # number of top k results to retrieve
        self.max_tokens = max_tokens  # max tokens per chunk

    def ingest_chunks(self, chunks: list[Knowledge]):
        """Ingest chunks into the knowledge base."""

        # check first 10 chunks
        print(f"First 10 chunks: {chunks[:10]}")
        i = 0
        for chunk in chunks:
            print(f"Chunk {i}: {chunk.knowledge}")
            i += 1
            if i > 10:
                break

        texts = [text for chunk in chunks for text in chunk.knowledge]

        # combine all chunks into a single string
        combined_text = "".join(texts)

        # tokenise
        token_ids = self.tokenizer.encode(combined_text)

        # chunk
        all_chunks: list[str] = []

        for i in range(0, len(token_ids), self.max_tokens):
            start = i
            end = i + self.max_tokens
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

        # Search each document index separately
        distance, index = self.index.search(np.array(query_emb), self.top_k)
        chunks = self.chunks
        for dist, idx in zip(distance[0], index[0]):

            # check if index is valid
            if idx < len(chunks):
                combined_results.append((dist, chunks[idx]))

        # sort all results by distance and return top_k overall
        combined_results.sort(key=lambda x: x[0])

        top_chunks = [
            Knowledge(text, source) for _, text in combined_results[: self.top_k]
        ]

        return top_chunks

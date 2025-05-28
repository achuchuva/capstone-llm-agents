from capabilities.knowledge_base import KnowledgeBase, Knowledge, Document, Folder
from sentence_transformers import SentenceTransformer
from transformers import GPT2TokenizerFast  # for token counting
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document as DocxDocument
import os, fitz, faiss, numpy as np


class FAISSKnowledgeBase(KnowledgeBase):
    """A knowledge base with per-document max_tokens and top_k support."""

    def __init__(
        self,
        supported_extensions: list[str],
        default_max_tokens: int = 100,
        default_top_k: int = 5,
        path_keywords: list[str] = None,
        reference_text: str = None,
        similarity_threshold: float = 0.5,
    ):
        super().__init__("knowledge_base")
        self.supported_extensions = supported_extensions
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.documents = []  # Each document stores its own settings and index
        self.default_max_tokens = default_max_tokens
        self.default_top_k = default_top_k
        self.path_keywords = path_keywords or []
        self.similarity_threshold = similarity_threshold
        self.reference_embedding = None

        if reference_text:
            self.reference_embedding = self.model.encode([reference_text])[0]

    def is_supported_extension(self, extension: str) -> bool:
        return extension in self.supported_extensions

    def _passes_path_filter(self, document: Document) -> bool:
        if not self.path_keywords:
            return True  # No filter applied

        path_parts = document.path.lower().split(os.sep)
        for part in path_parts:
            if any(keyword in part for keyword in self.path_keywords):
                return True
        return False

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

    def ingest_document(self, document: Document) -> bool:
        if not self.is_supported_extension(document.extension):
            raise ValueError(f"Unsupported file extension: {document.extension}")

        # === Path heuristic ===
        if not self._passes_path_filter(document):
            print(
                f"Skipped '{document.path}' — path did not match sprint-related keywords."
            )
            return False

        # === Extract text ===
        texts = []
        if document.extension == "pdf":
            doc = fitz.open(document.path)
            for page in doc:
                texts.append(page.get_text())
        elif document.extension == "docx":
            doc = DocxDocument(document.path)
            texts = [para.text for para in doc.paragraphs if para.text.strip()]
        else:
            with open(document.path, "r", encoding="utf-8") as f:
                texts = [f.read()]

        full_text = "\n".join(texts)

        # === Similarity check ===
        if self.reference_embedding is not None:
            snippet = full_text[:1000]  # ~1000 characters snippet for similarity check
            snippet_embedding = self.model.encode([snippet])[0]
            similarity = cosine_similarity(
                [self.reference_embedding], [snippet_embedding]
            )[0][0]

            if similarity < self.similarity_threshold:
                print(
                    f"Skipped '{document.path}' — similarity {similarity:.2f} < threshold {self.similarity_threshold}"
                )
                return False
            else:
                print(f"Accepted '{document.path}' — similarity {similarity:.2f}")

        # === Tokenization ===
        token_ids = self.tokenizer.encode(full_text)
        total_tokens = len(token_ids)

        # === Heuristics ===
        max_tokens, top_k = self._estimate_document_heuristics(total_tokens)

        # === Chunking ===
        all_chunks = []
        for i in range(0, total_tokens, max_tokens):
            chunk_ids = token_ids[i : i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_ids)
            all_chunks.append(chunk_text)

        if not all_chunks:
            print(f"Skipped '{document.path}' — no valid chunks created.")
            return False

        # === Embeddings & Indexing ===
        embeddings = self.model.encode(all_chunks)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings))
        timestamp = os.path.getmtime(document.path)

        self.documents.append(
            {
                "path": document.path,
                "chunks": all_chunks,
                "embeddings": embeddings,
                "index": index,
                "max_tokens": max_tokens,
                "top_k": top_k,
                "length": total_tokens,
                "timestamps": [timestamp] * len(all_chunks),
                "document": document,
            }
        )

        print(
            f"Ingested document ({total_tokens} tokens) with {len(all_chunks)} chunks, "
            f"max_tokens={max_tokens}, top_k={top_k}."
        )
        return True

    def ingest_folder(self, folder: Folder) -> list[Document]:
        """Ingests all supported documents in a given folder."""
        documents = folder.get_documents()
        ingested_documents = []

        for document in documents:
            try:
                ingested = self.ingest_document(document)
            except Exception as e:
                print(f"[ERROR] Failed to ingest {document.path}: {e}")
            else:
                if ingested:
                    ingested_documents.append(document)

        return ingested_documents

    def update_folder(self, folder: Folder) -> list[Document]:
        """Update the knowledge base with new, modified, or deleted documents from a folder."""

        current_doc_paths = {doc["path"]: doc for doc in self.documents}
        folder_documents = folder.get_documents()

        # Paths of documents currently in the folder
        folder_paths = {doc.path for doc in folder_documents}

        new_documents = []
        modified_documents = []

        # Step 1: Identify new and modified documents
        for document in folder_documents:
            if document.path not in current_doc_paths:
                new_documents.append(document)
            else:
                current_timestamp = os.path.getmtime(document.path)
                if (
                    current_timestamp
                    > current_doc_paths[document.path]["timestamps"][0]
                ):
                    modified_documents.append(document)

        # Step 2: Identify and remove deleted documents
        deleted_docs = []

        deleted_paths = set(current_doc_paths.keys()) - folder_paths
        if deleted_paths:
            print(f"[INFO] Deleted documents: {deleted_paths}")

        for path in deleted_paths:
            deleted_docs.append(current_doc_paths[path]["document"])

        self.documents = [
            doc for doc in self.documents if doc["path"] not in deleted_paths
        ]

        # Step 3: Remove outdated entries for modified documents
        modified_paths = {doc.path for doc in modified_documents}
        self.documents = [
            doc for doc in self.documents if doc["path"] not in modified_paths
        ]

        # Step 4: Log updates
        for new_doc in new_documents:
            print(f"[INFO] New document found: {new_doc.path}")
        for mod_doc in modified_documents:
            print(f"[INFO] Modified document found: {mod_doc.path}")

        # Step 5: Ingest new and modified documents
        for document in new_documents + modified_documents:
            try:
                self.ingest_document(document)
            except Exception as e:
                print(f"[ERROR] Failed to update {document.path}: {e}")

        return deleted_docs

    def group_similar_chunks(
        self,
        chunks: list[str],
        embeddings: list,
        timestamps: list[float],
        similarity_threshold: float = 0.85,
    ) -> list[str]:
        """
        Groups similar chunks using cosine similarity and returns the most recent chunk from each group.

        Args:
            chunks: List of text chunks.
            embeddings: List of vector embeddings corresponding to chunks.
            timestamps: List of timestamps (floats) for each chunk.
            similarity_threshold: Cosine similarity threshold for grouping.

        Returns:
            A list of representative chunks, one from each group.
        """
        if not chunks:
            return []

        sim_matrix = cosine_similarity(embeddings)
        n = len(chunks)
        visited = set()
        groups = []

        for i in range(n):
            if i in visited:
                continue
            group = [i]
            visited.add(i)
            for j in range(i + 1, n):
                if j not in visited and sim_matrix[i][j] >= similarity_threshold:
                    group.append(j)
                    visited.add(j)
            groups.append(group)

        # Select the most recent chunk from each group
        selected_chunks = []
        for group in groups:
            latest_idx = max(group, key=lambda idx: timestamps[idx])
            selected_chunks.append(chunks[latest_idx])

        return selected_chunks

    def retrieve_related_knowledge(self, query: str) -> list[Knowledge]:
        if not self.documents:
            return []

        query_emb = self.model.encode([query])
        candidate_chunks = []
        candidate_embs = []
        candidate_times = []

        for doc in self.documents:
            D, I = doc["index"].search(np.array(query_emb), doc["top_k"])
            for dist, idx in zip(D[0], I[0]):
                if idx < len(doc["chunks"]):
                    candidate_chunks.append(doc["chunks"][idx])
                    candidate_embs.append(doc["embeddings"][idx])
                    candidate_times.append(doc["timestamps"][idx])

        # Group and filter conflicting/similar chunks
        selected_chunks = self.group_similar_chunks(
            candidate_chunks, candidate_embs, candidate_times
        )

        # Rank final selected chunks by similarity to query
        final_embs = self.model.encode(selected_chunks)
        similarities = cosine_similarity([query_emb[0]], final_embs)[0]
        top_indices = np.argsort(similarities)[-self.default_top_k :][::-1]

        return [Knowledge(selected_chunks[i]) for i in top_indices]

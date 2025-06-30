import faiss
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

class SemanticPaperDB:
    # Added embedding_file and metadata_file as optional parameters for easier testing
    def __init__(self, embedding_file="paper_index.faiss", metadata_file="paper_metadata.json"):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.IndexFlatIP(384)  # Cosine similarity via normalized vectors
        self.metadata = []

        self.embedding_file = embedding_file
        self.metadata_file = metadata_file

        if os.path.exists(self.embedding_file) and os.path.exists(self.metadata_file):
            self.index = faiss.read_index(self.embedding_file)
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)

            if self.index.ntotal != len(self.metadata):
                print(f"Warning: index size {self.index.ntotal} != metadata size {len(self.metadata)}")

    def _normalize(self, embedding):
        return embedding / np.linalg.norm(embedding, axis=1, keepdims=True)

    def add_paper(self, paper_id, summary, title="", year=""):
        if any(item["paper_id"] == paper_id for item in self.metadata):
            print(f"Paper {paper_id} already exists, skipping.")
            return

        embedding = self.model.encode([summary])
        embedding = self._normalize(np.array(embedding).astype("float32"))
        self.index.add(embedding)

        self.metadata.append({
            "paper_id": paper_id,
            "summary": summary,
            "title": title,
            "year": year
        })

        faiss.write_index(self.index, self.embedding_file)
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def search(self, query, k=3):
        if self.index.ntotal == 0:
            return []

        embedding = self.model.encode([query])
        embedding = self._normalize(np.array(embedding).astype("float32"))
        D, I = self.index.search(embedding, k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]

    def search_similar_by_paper_id(self, paper_id, k=3):
        if len(self.metadata) <= 1:
            return []

        for i, item in enumerate(self.metadata):
            if item["paper_id"] == paper_id:
                embedding = self.model.encode([item["summary"]])
                embedding = self._normalize(np.array(embedding).astype("float32"))
                D, I = self.index.search(embedding, k + 1)

                results = []
                for idx in I[0]:
                    if idx != i:
                        results.append(self.metadata[idx])
                    if len(results) == k:
                        break

                return results
        return []

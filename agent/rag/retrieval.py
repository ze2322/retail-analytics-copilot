<<<<<<< HEAD
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class Retriever:
    def __init__(self, docs_folder="docs/", top_k=3):
        self.docs_folder = docs_folder
        self.top_k = top_k
        self.chunks = []
        self.vectorizer = None
        self.doc_matrix = None
        self._load_docs()

    def _load_docs(self):
        chunk_id = 0
        for fname in os.listdir(self.docs_folder):
            if fname.endswith(".md"):
                base = os.path.splitext(fname)[0]
                with open(os.path.join(self.docs_folder, fname), "r", encoding="utf-8") as f:
                    content = f.read().split("\n\n")  # simple paragraph chunks
                    for i, chunk in enumerate(content):
                        chunk = chunk.strip()
                        if chunk:
                            chunk_id = f"{base}::chunk{i}"
                            self.chunks.append({
                                "id": chunk_id,
                                "source": base,
                                "chunk_index": i,
                                "content": chunk
                            })
        self.vectorizer = TfidfVectorizer()
        self.doc_matrix = self.vectorizer.fit_transform([c["content"] for c in self.chunks])

    def retrieve(self, query):
        query_vec = self.vectorizer.transform([query])
        scores = np.dot(self.doc_matrix, query_vec.T).toarray().squeeze()
        top_indices = np.argsort(scores)[-self.top_k:][::-1]
        results = []
        for idx in top_indices:
            results.append({
                "chunk_id": self.chunks[idx]["id"],
                "source": self.chunks[idx].get("source"),
                "chunk_index": self.chunks[idx].get("chunk_index"),
                "content": self.chunks[idx]["content"],
                "score": float(scores[idx])
            })
        return results
=======
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class Retriever:
    def __init__(self, docs_folder="docs/", top_k=3):
        self.docs_folder = docs_folder
        self.top_k = top_k
        self.chunks = []
        self.vectorizer = None
        self.doc_matrix = None
        self._load_docs()

    def _load_docs(self):
        chunk_id = 0
        for fname in os.listdir(self.docs_folder):
            if fname.endswith(".md"):
                base = os.path.splitext(fname)[0]
                with open(os.path.join(self.docs_folder, fname), "r", encoding="utf-8") as f:
                    content = f.read().split("\n\n")  # simple paragraph chunks
                    for i, chunk in enumerate(content):
                        chunk = chunk.strip()
                        if chunk:
                            chunk_id = f"{base}::chunk{i}"
                            self.chunks.append({
                                "id": chunk_id,
                                "source": base,
                                "chunk_index": i,
                                "content": chunk
                            })
        self.vectorizer = TfidfVectorizer()
        self.doc_matrix = self.vectorizer.fit_transform([c["content"] for c in self.chunks])

    def retrieve(self, query):
        query_vec = self.vectorizer.transform([query])
        scores = np.dot(self.doc_matrix, query_vec.T).toarray().squeeze()
        top_indices = np.argsort(scores)[-self.top_k:][::-1]
        results = []
        for idx in top_indices:
            results.append({
                "chunk_id": self.chunks[idx]["id"],
                "source": self.chunks[idx].get("source"),
                "chunk_index": self.chunks[idx].get("chunk_index"),
                "content": self.chunks[idx]["content"],
                "score": float(scores[idx])
            })
        return results
>>>>>>> 8e017c34374abf24b249e7e3dbbfa14b453c5c75

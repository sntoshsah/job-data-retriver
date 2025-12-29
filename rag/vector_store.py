import faiss
import numpy as np
import pickle

class FAISSVectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.texts = []
        self.metadata = []

    def add(self, embeddings, texts, metadatas):
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)
        self.metadata.extend(metadatas)

    def search(self, query_embedding, top_k=5):
        scores, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            top_k
        )

        results = []
        for idx, score in zip(indices[0], scores[0]):
            results.append({
                "score": float(score),
                "text": self.texts[idx],
                **self.metadata[idx]
            })
        return results

    def save(self, index_path, meta_path):
        faiss.write_index(self.index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump(
                {"texts": self.texts, "metadata": self.metadata},
                f
            )

    @classmethod
    def load(cls, index_path, meta_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            data = pickle.load(f)

        store = cls(index.d)
        store.index = index
        store.texts = data["texts"]
        store.metadata = data["metadata"]
        return store

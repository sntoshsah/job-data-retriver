from rag.embedding import HFEmbeddingModel

class Retriever:
    def __init__(self, store):
        self.store = store
        self.embedder = HFEmbeddingModel()

    def retrieve(self, query, top_k=5):
        query_emb = self.embedder.encode([query])[0]
        return self.store.search(query_emb, top_k)

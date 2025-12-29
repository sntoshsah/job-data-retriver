import pandas as pd
from rag.preprocessing import preprocess_description
from rag.chunking import chunk_text
from rag.embedding import HFEmbeddingModel
from rag.vector_store import FAISSVectorStore
import os



embedder = HFEmbeddingModel()
documents, metadatas = [], []
def data_ingestion():
    df = pd.read_excel("data/LF Jobs.xlsx")
    for _, row in df.iterrows():
        cleaned = preprocess_description(row["Job Description"])
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            documents.append(chunk)
            metadatas.append({
                "job_id": row["ID"],
                "title": row["Job Title"],
                "company": row["Company Name"],
                "location": row["Job Location"],
                "level": row["Job Level"],
                "category": row["Job Category"],
                "tags": row["Tags"]
            })

    embeddings = embedder.encode(documents)

    store = FAISSVectorStore(dim=embeddings.shape[1])
    store.add(embeddings, documents, metadatas)

    store.save(
        index_path="data/job_index.faiss",
        meta_path="data/job_metadata.pkl"
    )

    print("Ingestion complete.")


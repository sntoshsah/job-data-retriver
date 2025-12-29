import os
from fastapi import FastAPI
from app.schemas import QueryRequest
from rag.retriever import Retriever
from rag.prompt import build_prompt
from rag.llm import HFLLM
from rag.vector_store import FAISSVectorStore
from scripts.ingest import data_ingestion

app = FastAPI(title="Job Data Retriever (RAG)")

DATA_DIR = "data"
INDEX_FILE = "job_index.faiss"
META_FILE = "job_metadata.pkl"

store: FAISSVectorStore | None = None
retriever: Retriever | None = None
llm: HFLLM | None = None


@app.on_event("startup")
def startup_event():
    global store, retriever, llm

    index_path = os.path.join(DATA_DIR, INDEX_FILE)
    meta_path = os.path.join(DATA_DIR, META_FILE)

    # 1 Ensure data exists
    if not (os.path.exists(index_path) and os.path.exists(meta_path)):
        print("⏳ Running data ingestion...")
        data_ingestion()
        print("Data ingestion completed.")
    else:
        print("Data already ingested. Skipping ingestion.")

    # 2 Load FAISS store
    store = FAISSVectorStore.load(
        index_path=index_path,
        meta_path=meta_path
    )

    # 3 Initialize retriever & LLM
    retriever = Retriever(store)
    llm = HFLLM()

    print("🚀 Job RAG API ready")


def sanitize_for_json(obj):
    if isinstance(obj, float) and obj != obj:
        return None
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_for_json(i) for i in obj]
    return obj


@app.post("/api/query", tags=["RAG"])
def query_jobs(req: QueryRequest):
    docs = retriever.retrieve(req.query, req.top_k)
    prompt = build_prompt(req.query, docs)
    answer = llm.generate(prompt)

    return sanitize_for_json({
        "query": req.query,
        "jobs": docs,
        "answer": answer
    })

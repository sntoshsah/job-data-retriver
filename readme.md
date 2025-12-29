# Job Data Retriever with RAG

A Retrieval-Augmented Generation (RAG) system for job data retrieval using Hugging Face models and FastAPI.

## Description

This project implements a RAG-based API for retrieving and generating responses about job listings. It uses FAISS for vector storage, Hugging Face embeddings and language models, and provides a FastAPI interface for querying job data.

## Features

- **Data Ingestion**: Processes job data from Excel files, cleans and chunks text, generates embeddings.
- **Vector Storage**: Uses FAISS for efficient similarity search on job descriptions.
- **Retrieval**: Retrieves relevant job chunks based on user queries.
- **Generation**: Uses Hugging Face LLMs to generate contextual responses.
- **API**: FastAPI-based REST API for easy integration.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:sntoshsah/job-data-retriver.git
   cd GenAI_task
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the job data file `data/LF Jobs.xlsx` in the data directory.

## Usage

### Running the API

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- **GET /**: Health check endpoint.
- **POST /query**: Query the RAG system with a job-related question.

Example request:
```json
{
  "query": "What are some software engineering jobs in New York?"
}
```

### Data Ingestion

If the vector store doesn't exist, it will be created automatically on startup. You can also run ingestion manually:
```python
from scripts.ingest import data_ingestion
data_ingestion()
```

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── schemas.py       # Pydantic models
├── data/
│   └── job_index.faiss  # FAISS vector index
├── notebook/
│   └── test.ipynb       # Jupyter notebook for testing
├── rag/
│   ├── __init__.py
│   ├── chunking.py      # Text chunking utilities
│   ├── embedding.py     # Hugging Face embedding model
│   ├── llm.py           # Hugging Face language model
│   ├── preprocessing.py # Text preprocessing
│   ├── prompt.py        # Prompt building
│   ├── retriever.py     # Retrieval logic
│   └── vector_store.py  # FAISS vector store wrapper
├── scripts/
│   ├── __init__.py
│   └── ingest.py        # Data ingestion script
├── requirements.txt     # Python dependencies
└── readme.md            # This file
```

## Dependencies

- fastapi: Web framework
- huggingface: Hugging Face libraries
- faiss-cpu: Vector similarity search
- sentence-transformers: Embedding models
- pandas: Data processing
- And more (see requirements.txt)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.
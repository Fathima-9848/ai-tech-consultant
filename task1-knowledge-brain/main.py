
import json
import importlib.util
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from fastapi import FastAPI, Query, HTTPException
from sentence_transformers import SentenceTransformer

app = FastAPI(title="AI Tech Consultant - Knowledge Brain")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent

EMBEDDINGS_FILE = (
    BASE_DIR / "documents" / "embeddings" / "chunk_embeddings.npy"
)
METADATA_FILE = (
    BASE_DIR / "documents" / "embeddings" / "chunk_metadata.jsonl"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load the RAG router from rag.py in this same folder.
RAG_FILE = BASE_DIR / "rag.py"

if not RAG_FILE.exists():
    raise RuntimeError(f"RAG file not found: {RAG_FILE}")

spec = importlib.util.spec_from_file_location("rag_module", RAG_FILE)

if spec is None or spec.loader is None:
    raise RuntimeError("Could not load rag.py")

rag_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag_module)

app.include_router(rag_module.router)

model = None
embeddings = None
metadata = None


def load_search_data():
    global model, embeddings, metadata

    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    if embeddings is None:
        embeddings = np.load(EMBEDDINGS_FILE)

    if metadata is None:
        with METADATA_FILE.open("r", encoding="utf-8") as file:
            metadata = [
                json.loads(line)
                for line in file
                if line.strip()
            ]

    if len(embeddings) != len(metadata):
        raise RuntimeError(
            "Embedding count and metadata count do not match."
        )


@app.get("/")
def home():
    return {
        "message": "AI Tech Consultant Knowledge Brain is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/search")
def search(
    q: str = Query(
        ...,
        min_length=2,
        description="Your question"
    ),
    top_k: int = Query(3, ge=1, le=10)
):
    try:
        load_search_data()

        query_vector = model.encode(
            [q],
            convert_to_numpy=True,
            normalize_embeddings=True
        )[0]

        scores = embeddings @ query_vector
        best_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in best_indices:
            item = metadata[int(index)]

            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "text": item.get("text", ""),
                "score": round(float(scores[index]), 4)
            })

        return {
            "query": q,
            "results_count": len(results),
            "results": results
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Embedding or metadata files were not found."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(error)}"
        )


import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]

CHUNKS_FILE = BASE_DIR / "documents" / "chunks" / "chunks.jsonl"
OUTPUT_DIR = BASE_DIR / "documents" / "embeddings"
OUTPUT_FILE = OUTPUT_DIR / "chunk_embeddings.npy"
METADATA_FILE = OUTPUT_DIR / "chunk_metadata.jsonl"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32

def main():
    if not CHUNKS_FILE.exists():
        print(f"Chunks file not found: {CHUNKS_FILE}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading chunks...")

    chunks = []
    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                chunks.append(json.loads(line))

    if not chunks:
        print("No chunks found.")
        return

    texts = [chunk["text"] for chunk in chunks]

    print(f"Total chunks: {len(texts)}")
    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings. Please wait...")

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    np.save(OUTPUT_FILE, embeddings)

    with METADATA_FILE.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print("\nEmbeddings created successfully!")
    print(f"Chunks processed: {len(chunks)}")
    print(f"Embedding dimensions: {embeddings.shape[1]}")
    print(f"Embeddings saved to: {OUTPUT_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")

if __name__ == "__main__":
    main()

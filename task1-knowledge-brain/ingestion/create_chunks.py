
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = BASE_DIR / "documents" / "cleaned_articles"
OUTPUT_DIR = BASE_DIR / "documents" / "chunks"
OUTPUT_FILE = OUTPUT_DIR / "chunks.jsonl"

CHUNK_SIZE = 1000
OVERLAP = 150

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

total_articles = 0
total_chunks = 0
failed = 0

with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
    for file_path in INPUT_DIR.glob("*.txt"):
        try:
            with file_path.open("r", encoding="utf-8") as file:
                article = json.load(file)

            text = article.get("text", "").strip()

            if not text:
                continue

            total_articles += 1
            start = 0
            chunk_index = 0

            while start < len(text):
                end = min(start + CHUNK_SIZE, len(text))

                # Try to finish at a word boundary
                if end < len(text):
                    space_position = text.rfind(
                        " ", start + CHUNK_SIZE - 150, end
                    )
                    if space_position > start:
                        end = space_position

                chunk_text = text[start:end].strip()

                if chunk_text:
                    record = {
                        "chunk_id": f"{file_path.stem}_{chunk_index}",
                        "source_file": file_path.name,
                        "title": article.get("title", ""),
                        "url": article.get("url", ""),
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                        "images": article.get("images", []),
                    }

                    output_file.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )

                    total_chunks += 1
                    chunk_index += 1

                if end >= len(text):
                    break

                start = max(0, end - OVERLAP)

        except (json.JSONDecodeError, OSError, TypeError) as error:
            failed += 1
            print(f"Could not process {file_path.name}: {error}")

print("\nChunking completed!")
print(f"Articles processed: {total_articles}")
print(f"Total chunks created: {total_chunks}")
print(f"Failed articles: {failed}")
print(f"Output file: {OUTPUT_FILE}")


import json
import re
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "documents" / "articles"
OUTPUT_DIR = BASE_DIR / "documents" / "cleaned_articles"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Website footer text that should not be part of the article
FOOTER_MARKERS = [
    "Was this article helpful and accurate?",
    "Was this article helpful?",
    "Help us improve this article with their feedback.",
    "Help us improve this article with your feedback.",
    "Related Articles",
]

successful = 0
failed = 0
empty = 0

for file_path in INPUT_DIR.glob("*.txt"):
    try:
        with file_path.open("r", encoding="utf-8") as file:
            article = json.load(file)

        text = article.get("text", "")

        # Remove the article's extra Link line
        text = re.sub(
            r"Link:\s*https?://\S+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Remove feedback and related-article sections
        cut_positions = [
            text.find(marker)
            for marker in FOOTER_MARKERS
            if text.find(marker) != -1
        ]

        if cut_positions:
            text = text[:min(cut_positions)]

        # Clean extra spaces and blank lines
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            empty += 1
            continue

        article["text"] = text

        output_path = OUTPUT_DIR / file_path.name
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(article, file, ensure_ascii=False, indent=2)

        successful += 1

    except (json.JSONDecodeError, OSError, TypeError, AttributeError) as error:
        failed += 1
        print(f"Could not process {file_path.name}: {error}")

print("\nArticle cleaning completed!")
print(f"Cleaned successfully: {successful}")
print(f"Empty articles skipped: {empty}")
print(f"Failed articles: {failed}")
print(f"Output folder: {OUTPUT_DIR}")


from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
import re
import time
import json

BASE_DIR = Path(__file__).resolve().parent
URL_FILE = BASE_DIR / "solution_urls.txt"
OUTPUT_DIR = BASE_DIR.parent / "documents" / "articles"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_parts = []
        self.article_parts = []
        self.image_urls = []
        self.in_title = False
        self.in_article = False
        self.article_depth = 0
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True

        if tag == "article" and attrs.get("id") == "article-body":
            self.in_article = True
            self.article_depth = 1
            return

        if self.in_article:
            if tag in ("script", "style", "noscript"):
                self.skip_depth += 1

            if tag == "img":
                image_url = attrs.get("src") or attrs.get("data-src")
                if image_url:
                    self.image_urls.append(image_url)

            self.article_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

        if self.in_article:
            if tag in ("script", "style", "noscript"):
                self.skip_depth = max(0, self.skip_depth - 1)

            self.article_depth -= 1

            if self.article_depth <= 0:
                self.in_article = False
                self.article_depth = 0

    def handle_data(self, data):
        value = data.strip()

        if self.in_title and value:
            self.title_parts.append(value)

        if self.in_article and self.skip_depth == 0 and value:
            self.article_parts.append(value)


urls = URL_FILE.read_text(encoding="utf-8").splitlines()
article_urls = [
    url for url in urls
    if "/support/solutions/articles/" in url
]

success = 0
failed = 0
manifest = []

for number, url in enumerate(article_urls, start=1):
    article_id_match = re.search(r"/articles/(\d+)", url)

    if not article_id_match:
        continue

    article_id = article_id_match.group(1)
    output_file = OUTPUT_DIR / f"{article_id}.txt"

    try:
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(request, timeout=20) as response:
            html = response.read().decode("utf-8", errors="replace")

        parser = ArticleParser()
        parser.feed(html)
        parser.close()

        title = " ".join(parser.title_parts)
        text = re.sub(
            r"\s+", " ", " ".join(parser.article_parts)
        ).strip()

        if not text:
            failed += 1
            manifest.append({
                "url": url,
                "status": "NO_ARTICLE_TEXT"
            })
            print(f"{number}/{len(article_urls)} - No article text")
            continue

        record = {
            "url": url,
            "title": title,
            "text": text,
            "images": parser.image_urls
        }

        output_file.write_text(
            json.dumps(record, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        success += 1
        manifest.append({
            "url": url,
            "title": title,
            "file": output_file.name,
            "status": "OK"
        })

        print(f"{number}/{len(article_urls)} - Saved: {article_id}")

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        failed += 1
        manifest.append({
            "url": url,
            "status": "ERROR",
            "error": str(error)
        })
        print(f"{number}/{len(article_urls)} - Failed: {article_id_match.group(1)}")

    time.sleep(0.2)

manifest_file = OUTPUT_DIR / "manifest.json"
manifest_file.write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("\nDownload completed!")
print("Article URLs:", len(article_urls))
print("Successful:", success)
print("Failed or empty:", failed)
print("Saved folder:", OUTPUT_DIR)
print("Manifest:", manifest_file)

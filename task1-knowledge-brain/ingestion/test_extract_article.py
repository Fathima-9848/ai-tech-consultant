
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from pathlib import Path
import re

url = (
    "https://support.brilliantdirectories.com/support/solutions/"
    "articles/5000558357-can-i-send-a-mass-email-campaign-using-brilliant-directories-"
)


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
        text = data.strip()

        if self.in_title and text:
            self.title_parts.append(text)

        if self.in_article and self.skip_depth == 0 and text:
            self.article_parts.append(text)


request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")

parser = ArticleParser()
parser.feed(html)
parser.close()

title = " ".join(parser.title_parts)
article_text = re.sub(
    r"\s+", " ", " ".join(parser.article_parts)
).strip()

output_file = Path(__file__).resolve().parent / "test_article_output.txt"

output_file.write_text(
    f"URL: {url}\n"
    f"TITLE: {title}\n"
    f"TEXT LENGTH: {len(article_text)} characters\n"
    f"IMAGE COUNT: {len(parser.image_urls)}\n\n"
    f"ARTICLE TEXT:\n{article_text}\n\n"
    f"IMAGE URLS:\n" + "\n".join(parser.image_urls),
    encoding="utf-8"
)

print("Title:", title)
print("Article text length:", len(article_text), "characters")
print("Images found inside article:", len(parser.image_urls))
print("Saved to:", output_file)

if not article_text:
    print("WARNING: Article text was not found. Check the HTML structure.")

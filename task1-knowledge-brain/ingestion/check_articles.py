
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
import time

folder = Path(__file__).resolve().parent
input_file = folder / "solution_urls.txt"
output_file = folder / "article_check_results.txt"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_parts = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data.strip())

urls = input_file.read_text(encoding="utf-8").splitlines()
results = []

for number, url in enumerate(urls, start=1):
    try:
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(request, timeout=15) as response:
            html = response.read().decode("utf-8", errors="replace")

        parser = PageParser()
        parser.feed(html)
        title = " ".join(parser.title_parts) or "No title found"

        results.append(f"URL: {url}\nTITLE: {title}\nSTATUS: OK\n")
        print(f"{number}/{len(urls)} - Checked")

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        results.append(
            f"URL: {url}\nTITLE: Not available\nSTATUS: ERROR - {error}\n"
        )
        print(f"{number}/{len(urls)} - Could not access")

    time.sleep(0.2)

output_file.write_text("\n".join(results), encoding="utf-8")

print("\nChecking completed!")
print("Results saved to:", output_file)

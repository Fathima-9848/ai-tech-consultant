
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re

url = "https://support.brilliantdirectories.com/support/solutions/articles/5000558357-can-i-send-a-mass-email-campaign-using-brilliant-directories-"

request = Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urlopen(request, timeout=20) as response:
    html = response.read().decode("utf-8", errors="replace")


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.matches = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id", "")
        classes = attrs.get("class", "")

        if element_id or classes:
            description = (
                f"TAG: {tag} | ID: {element_id} | CLASS: {classes}"
            )

            if re.search(
                r"article|solution|content|answer|description|body",
                f"{element_id} {classes}",
                re.IGNORECASE
            ):
                self.matches.append(description)


parser = StructureParser()
parser.feed(html)

print("Matching HTML elements:", len(parser.matches))

for item in parser.matches[:60]:
    print(item)

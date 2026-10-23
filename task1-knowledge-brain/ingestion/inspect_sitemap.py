
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

SITEMAP_URL = (
    "https://support.brilliantdirectories.com/support/sitemap.xml"
)

OUTPUT_FILE = Path(__file__).resolve().parent / "sitemap_urls.txt"


def inspect_sitemap():
    request = Request(
        SITEMAP_URL,
        headers={"User-Agent": "AI-Tech-Consultant/1.0"},
    )

    try:
        with urlopen(request, timeout=20) as response:
            xml_content = response.read()

        root = ElementTree.fromstring(xml_content)

        urls = [
            element.text.strip()
            for element in root.iter()
            if element.tag.endswith("loc") and element.text
        ]

        OUTPUT_FILE.write_text(
            "\n".join(urls),
            encoding="utf-8",
        )

        print("Sitemap successfully read!")
        print("URLs found:", len(urls))
        print("URLs saved to:", OUTPUT_FILE)

    except Exception as error:
        print("Could not read sitemap.")
        print("Reason:", error)


if __name__ == "__main__":
    inspect_sitemap()

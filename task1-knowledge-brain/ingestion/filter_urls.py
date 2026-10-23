
from pathlib import Path

# Read all URLs collected from the sitemap
folder = Path(__file__).resolve().parent
input_file = folder / "sitemap_urls.txt"

folder_file = folder / "folder_urls.txt"
solution_file = folder / "solution_urls.txt"
other_file = folder / "other_urls.txt"

urls = input_file.read_text(encoding="utf-8").splitlines()

folder_urls = []
solution_urls = []
other_urls = []

for url in urls:
    if "/support/solutions/folders/" in url:
        folder_urls.append(url)
    elif "/support/solutions/" in url and url.rstrip("/").split("/")[-1]:
        solution_urls.append(url)
    else:
        other_urls.append(url)

folder_file.write_text("\n".join(folder_urls), encoding="utf-8")
solution_file.write_text("\n".join(solution_urls), encoding="utf-8")
other_file.write_text("\n".join(other_urls), encoding="utf-8")

print("Total URLs:", len(urls))
print("Folder URLs:", len(folder_urls))
print("Solution URLs:", len(solution_urls))
print("Other URLs:", len(other_urls))
print("\nURL lists saved successfully!")

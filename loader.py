from pathlib import Path

def load_postings(file_path):
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    parts = content.split("----------")
    cleaned =[item.strip() for item in parts if item.strip()]
    return cleaned
postings = load_postings("data/sample/postings.txt")
print(len(postings))
for posting in postings:
    print(posting)
    print()
    print()

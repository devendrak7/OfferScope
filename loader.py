from pathlib import Path

def load_postings(file_path):
    path = Path(file_path)
    try :
        content = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print("Error: File not found.")
        return []
    parts = content.split("----------")
    cleaned =[item.strip() for item in parts if item.strip()]
    return cleaned



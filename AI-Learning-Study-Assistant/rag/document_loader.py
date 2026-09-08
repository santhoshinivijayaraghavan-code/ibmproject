import os
from pypdf import PdfReader

def load_documents(path, chunk_size=1000, overlap=150):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        return []

    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)

    return chunks

from pypdf import PdfReader

def load_pdf_pages(path):
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i+1, "text": text})
    return pages

def pdf_text(path):
    pages = load_pdf_pages(path)
    return "\n\n".join([f"Page {p['page']}:\n{p['text']}" for p in pages])

def pdf_to_docs(path):
    reader = PdfReader(path)
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            docs.append({"page": i+1, "text": text})
    return docs

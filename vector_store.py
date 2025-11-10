from pdf_utils import pdf_to_docs
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

def build_faiss(path, index_path="faiss_index"):
    docs = pdf_to_docs(path)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts, metadatas = [], []

    for d in docs:
        chunks = text_splitter.split_text(d["text"])
        for c in chunks:
            texts.append(c)
            metadatas.append({"page": d["page"]})

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(texts, emb, metadatas=metadatas)
    vector_store.save_local(index_path)
    return vector_store

def load_faiss(index_path="faiss_index"):
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_path, embeddings=emb, allow_dangerous_deserialization=True)

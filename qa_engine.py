from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from vector_store import load_faiss

def get_llm():
    return ChatGroq(
        groq_api_key="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",  # 🔒 replace with environment variable in production
        model="llama-3.1-8b-instant",
        temperature=0.0,
        max_tokens=512
    )

def load_qa(index_path="faiss_index"):
    index = load_faiss(index_path)
    retriever = index.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template("""
You are a helpful policy assistant.
Answer using ONLY the provided documents.

Documents:
{context}

Question:
{question}

If answer is not found in the documents, reply with:
"I don’t know based on the provided documents."
""")

    llm = get_llm()
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return chain

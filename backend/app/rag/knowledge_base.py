from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_FILE = BASE_DIR / "data" / "knowledge-base" / "banking_policies.txt"


def build_vector_store():
    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    documents = splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    return FAISS.from_documents(documents, embeddings)


vector_store = build_vector_store()


def search_knowledge_base(query: str, k: int = 3):
    documents = vector_store.similarity_search(query, k=k)

    return [doc.page_content for doc in documents]
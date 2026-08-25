import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Support both:
# 1. Local development
#    <project-root>/data/knowledge-base/banking_policies.txt
#
# 2. Cloud Run
#    /app/data/knowledge-base/banking_policies.txt

CURRENT_FILE = Path(__file__).resolve()

KNOWLEDGE_FILE_CANDIDATES = [
    # Cloud Run container
    Path("/app/data/knowledge-base/banking_policies.txt"),

    # Local project
    CURRENT_FILE.parents[3]
    / "data"
    / "knowledge-base"
    / "banking_policies.txt",
]

KNOWLEDGE_FILE = next(
    (
        path
        for path in KNOWLEDGE_FILE_CANDIDATES
        if path.exists()
    ),
    KNOWLEDGE_FILE_CANDIDATES[0],
)


def build_vector_store():
    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_FILE}"
        )

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. "
            "Please add it to backend/.env"
        )

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    documents = splitter.create_documents([text])

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )

    return FAISS.from_documents(
        documents,
        embeddings,
    )


vector_store = build_vector_store()


def search_knowledge_base(
    query: str,
    k: int = 3,
):
    documents = vector_store.similarity_search(
        query,
        k=k,
    )

    return [
        document.page_content
        for document in documents
    ]
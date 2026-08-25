from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


PROJECT_ID = "cohort3-apac-505212"
LOCATION = "us-central1"


CURRENT_FILE = Path(__file__).resolve()

KNOWLEDGE_FILE_CANDIDATES = [
    Path("/app/data/knowledge-base/banking_policies.txt"),

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

    text = KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    documents = splitter.create_documents([text])

    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-005",
        project=PROJECT_ID,
        location=LOCATION,
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
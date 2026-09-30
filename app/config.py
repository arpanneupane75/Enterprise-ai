import os

from dotenv import load_dotenv


load_dotenv()

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv(
    "LANGSMITH_TRACING",
    "false",
)
LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "enterprise-rag",
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Add it to your .env file."
    )


LLM_MODEL = "openai/gpt-oss-120b"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "enterprise_documents"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 150

RETRIEVAL_K = 5
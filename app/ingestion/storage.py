import json
from pathlib import Path

from langchain_core.documents import Document


PROCESSED_DIR = Path("data/processed")
CHUNKS_FILE = PROCESSED_DIR / "chunks.json"


def save_chunks(documents: list[Document]) -> None:
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = []

    for document in documents:
        data.append(
            {
                "page_content": document.page_content,
                "metadata": document.metadata,
            }
        )

    CHUNKS_FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def load_chunks() -> list[Document]:
    data = json.loads(
        CHUNKS_FILE.read_text(
            encoding="utf-8"
        )
    )

    return [
        Document(
            page_content=item["page_content"],
            metadata=item["metadata"],
        )
        for item in data
    ]
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_OVERLAP, CHUNK_SIZE


def split_documents(
    documents: list[Document],
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = f"chunk_{index}"

        chunk.metadata["document_type"] = "employee_handbook"

        if "page" in chunk.metadata:
            chunk.metadata["page"] = int(chunk.metadata["page"]) + 1

    return chunks
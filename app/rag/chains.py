
import json

from langchain_core.documents import Document

from app.models.schemas import (
    EvidenceResponse,
    RAGResponse,
    Source,
)
from app.rag.llm import get_llm
from app.rag.prompts import RAG_PROMPT
from app.retrieval.context_expansion import expand_context
from app.retrieval.query_transform import transform_query
from app.retrieval.retriever import get_retriever
from app.retrieval.reranker import rerank_documents


def format_documents(
    documents: list[Document],
) -> str:

    formatted_documents = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source",
        )

        page = document.metadata.get(
            "page",
            "Unknown page",
        )

        chunk_id = document.metadata.get(
            "chunk_id",
            "Unknown chunk",
        )

        formatted_documents.append(
            f"""
Source: {source}
Page: {page}
Chunk: {chunk_id}

Content:
{document.page_content}
"""
        )

    return "\n\n---\n\n".join(
        formatted_documents
    )


def format_history(
    history: list,
) -> str:

    if not history:
        return "No previous conversation."

    formatted_history = []

    for message in history:

        role = getattr(
            message,
            "role",
            "user",
        )

        content = getattr(
            message,
            "content",
            "",
        )

        formatted_history.append(
            f"{role.capitalize()}: {content}"
        )

    return "\n".join(
        formatted_history
    )


def retrieve_documents(
    question: str,
    candidate_k: int | None = None,
    final_k: int = 3,
) -> list[tuple[Document, float]]:

    retrieval_query = transform_query(
        question
    )

    retriever = get_retriever(
        candidate_k
    )

    documents = retriever.invoke(
        retrieval_query
    )

    return rerank_documents(
        question=retrieval_query,
        documents=documents,
        top_k=final_k,
    )


def ask_question(
    question: str,
    history: list | None = None,
) -> RAGResponse:

    if history is None:
        history = []

    # --------------------------------------------------
    # 1. Build conversation context
    # --------------------------------------------------

    conversation_history = format_history(
        history
    )

    # --------------------------------------------------
    # 2. Create retrieval question
    # --------------------------------------------------

    retrieval_question = question

    if history:

        retrieval_question = (
            f"""
Previous conversation:
{conversation_history}

Current question:
{question}

Rewrite the current question as a standalone
question that includes the necessary context from
the previous conversation.
"""
        )

    # --------------------------------------------------
    # 3. Retrieve and rerank
    # --------------------------------------------------

    reranked_documents = retrieve_documents(
        retrieval_question
    )

    # --------------------------------------------------
    # 4. Expand context
    # --------------------------------------------------

    documents = expand_context(
        reranked_documents,
        window=2,
    )

    # --------------------------------------------------
    # 5. Build LLM context
    # --------------------------------------------------

    context = format_documents(
        documents
    )
    
    prompt_value = RAG_PROMPT.invoke(
    {
        "history": conversation_history,
        "context": context,
        "question": question,
    }
)
    

    # --------------------------------------------------
    # 6. Generate structured answer
    # --------------------------------------------------

    llm = get_llm()

    response = llm.invoke(
        prompt_value
    )

    try:

        parsed_response = EvidenceResponse.model_validate(
            json.loads(response.content)
        )

    except Exception:

        parsed_response = EvidenceResponse(
            answer=response.content,
            evidence_chunk_ids=[],
        )

    # --------------------------------------------------
    # 7. Validate evidence chunk IDs
    # --------------------------------------------------

    valid_chunks = {
        document.metadata.get("chunk_id"): document
        for document in documents
    }

    evidence_documents = []

    for chunk_id in parsed_response.evidence_chunk_ids:

        document = valid_chunks.get(
            chunk_id
        )

        if document is not None:

            evidence_documents.append(
                document
            )

    # --------------------------------------------------
    # 8. Build sources
    # --------------------------------------------------

    sources = []

    seen_sources = set()

    for document in evidence_documents:

        source = document.metadata.get(
            "source",
            "Unknown source",
        )

        page = document.metadata.get(
            "page",
        )

        chunk_id = document.metadata.get(
            "chunk_id",
        )

        source_key = (
            source,
            page,
            chunk_id,
        )

        if source_key in seen_sources:
            continue

        seen_sources.add(
            source_key
        )

        sources.append(
            Source(
                source=source,
                page=page,
                chunk_id=chunk_id,
                relevance_score=None,
            )
        )

    # --------------------------------------------------
    # 9. Return final structured response
    # --------------------------------------------------

    return RAGResponse(
        answer=parsed_response.answer,
        sources=sources,
    )


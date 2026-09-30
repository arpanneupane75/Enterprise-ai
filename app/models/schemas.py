from pydantic import BaseModel


class Source(BaseModel):
    source: str
    page: int | None = None
    chunk_id: str | None = None
    relevance_score: float | None = None


class EvidenceResponse(BaseModel):
    answer: str
    evidence_chunk_ids: list[str]


class RAGResponse(BaseModel):
    answer: str
    sources: list[Source]

from fastapi import FastAPI, HTTPException

from app.api.schemas import QuestionRequest
from app.models.schemas import RAGResponse
from app.rag.chains import ask_question


app = FastAPI(
    title="Enterprise RAG API",
    description="Document question-answering API powered by RAG.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/ask",
    response_model=RAGResponse,
)
def ask(request: QuestionRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:

        return ask_question(
            question=request.question,
            history=request.history,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline failed: {str(e)}",
        )


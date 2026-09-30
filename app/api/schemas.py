
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class QuestionRequest(BaseModel):
    question: str
    history: list[ChatMessage] = Field(default_factory=list)

"""
Schemas Pydantic para validación y serialización de datos.
"""
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """Schema para solicitud de sugerencia."""
    query: str = Field(..., min_length=1, description="Consulta del usuario")

    @field_validator('query')
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        return v.strip()


class SuggestionResponse(BaseModel):
    """Schema para respuesta de sugerencia."""
    query: str
    suggestion: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class HistoryEntry(BaseModel):
    """Schema para entrada del historial."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    query: str
    suggestion: str
    confidence: float


class HistoryResponse(BaseModel):
    """Schema para respuesta del historial."""
    total: int
    queries: List[HistoryEntry]


class KnowledgeEntry(BaseModel):
    """Schema para agregar conocimiento."""
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)

    @field_validator('question', 'answer')
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return v.strip()


class KnowledgeResponse(BaseModel):
    """Schema para respuesta al agregar conocimiento."""
    message: str
    total_entries: int


class HealthResponse(BaseModel):
    """Schema para health check."""
    status: str
    version: str
    knowledge_entries: int
    history_entries: int

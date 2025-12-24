"""
Router para el endpoint de administración de conocimiento.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models import KnowledgeEntry, KnowledgeResponse
from app.services import KnowledgeBase
from app.dependencies import get_knowledge_base
from app.config import logger

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.post("", response_model=KnowledgeResponse, status_code=201)
async def add_knowledge(
    entry: KnowledgeEntry,
    kb: KnowledgeBase = Depends(get_knowledge_base)
) -> KnowledgeResponse:
    """Agrega una nueva entrada a la base de conocimiento."""
    logger.info(f"Attempting to add knowledge: {entry.question[:50]}...")
    
    success = kb.add_entry(entry.question, entry.answer)
    
    if not success:
        logger.warning(f"Duplicate knowledge entry rejected: {entry.question}")
        raise HTTPException(status_code=409, detail="Esta pregunta ya existe.")
    
    total = kb.count()
    logger.info(f"Knowledge entry added successfully. Total entries: {total}")
    
    return KnowledgeResponse(message="Knowledge entry added successfully", total_entries=total)

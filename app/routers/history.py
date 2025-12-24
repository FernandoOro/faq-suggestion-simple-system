"""
Router para el endpoint de historial.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.models import HistoryResponse
from app.services import HistoryService
from app.dependencies import get_history_service
from app.config import logger

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=HistoryResponse)
def get_history(
    limit: Optional[int] = Query(None, ge=1),
    history: HistoryService = Depends(get_history_service)
) -> HistoryResponse:
    """Obtiene el historial de consultas realizadas."""
    logger.info(f"Retrieving history with limit={limit}")
    
    entries = history.get_history(limit=limit)
    total = history.count()
    
    logger.info(f"Returning {len(entries)} of {total} history entries")
    
    return HistoryResponse(total=total, queries=entries)

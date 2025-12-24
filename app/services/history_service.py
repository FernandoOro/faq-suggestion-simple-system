"""
Servicio de gestión del historial de consultas.
"""
from datetime import datetime
from typing import List, Optional
from app.models.schemas import HistoryEntry
from app.config import logger


class HistoryService:
    """Servicio Singleton para gestionar el historial de consultas en memoria."""
    
    def __init__(self):
        self._history: List[HistoryEntry] = []
        logger.info("HistoryService initialized")
    
    def add_entry(self, query: str, suggestion: str, confidence: float) -> None:
        """Agrega una entrada al historial."""
        entry = HistoryEntry(
            timestamp=datetime.utcnow(),
            query=query,
            suggestion=suggestion,
            confidence=confidence
        )
        self._history.append(entry)
        logger.debug(f"Added history entry for query: {query[:50]}...")
    
    def get_history(self, limit: Optional[int] = None) -> List[HistoryEntry]:
        """Obtiene el historial de consultas."""
        history = sorted(self._history, key=lambda x: x.timestamp, reverse=True)
        
        if limit:
            history = history[:limit]
        
        logger.info(f"Retrieved {len(history)} history entries")
        return history
    
    def count(self) -> int:
        """Retorna el número total de consultas en el historial."""
        return len(self._history)
    
    def clear(self) -> None:
        """Limpia el historial."""
        self._history.clear()
        logger.info("History cleared")

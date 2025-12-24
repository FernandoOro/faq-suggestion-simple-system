"""
Sistema de inyección de dependencias usando el patrón Singleton.
"""
from functools import lru_cache
from app.services import KnowledgeBase, SimilarityService, HistoryService


@lru_cache()
def get_knowledge_base() -> KnowledgeBase:
    return KnowledgeBase()


@lru_cache()
def get_similarity_service() -> SimilarityService:
    return SimilarityService(threshold=0.6)


@lru_cache()
def get_history_service() -> HistoryService:
    return HistoryService()

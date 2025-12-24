"""
Servicio de gestión de la base de conocimiento.
"""
from typing import Dict, Optional
from app.config import logger


class KnowledgeBase:
    """Servicio Singleton para gestionar la base de conocimiento en memoria."""
    
    def __init__(self):
        self._knowledge: Dict[str, str] = {}
        logger.info("KnowledgeBase initialized")
    
    def load_knowledge(self, knowledge_data: Dict[str, str]) -> None:
        """Carga el conocimiento inicial desde un diccionario."""
        self._knowledge = knowledge_data.copy()
        logger.info(f"Loaded {len(self._knowledge)} knowledge entries")
    
    def add_entry(self, question: str, answer: str) -> bool:
        """Agrega una nueva entrada a la base de conocimiento."""
        question_lower = question.lower()
        
        if question_lower in [q.lower() for q in self._knowledge.keys()]:
            logger.warning(f"Duplicate question attempted: {question}")
            return False
        
        self._knowledge[question] = answer
        logger.info(f"Added new knowledge entry: {question[:50]}...")
        return True
    
    def get_all_questions(self) -> list[str]:
        """Obtiene todas las preguntas disponibles."""
        return list(self._knowledge.keys())
    
    def get_answer(self, question: str) -> Optional[str]:
        """Obtiene la respuesta para una pregunta específica."""
        return self._knowledge.get(question)
    
    def count(self) -> int:
        """Retorna el número total de entradas."""
        return len(self._knowledge)

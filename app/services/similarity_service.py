"""
Servicio de búsqueda por similitud usando difflib.
"""
from difflib import SequenceMatcher
from typing import Tuple, Optional
from app.config import logger

# TODO: Si el dataset crece >1k entradas, considerar sentence-transformers
# difflib es O(n) por query, pero para FAQs pequeños es suficiente


class SimilarityService:
    """Servicio para encontrar la pregunta más similar."""
    
    def __init__(self, threshold: float = 0.6):
        self.threshold = threshold
        logger.info(f"SimilarityService initialized with threshold={threshold}")
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calcula la similitud entre dos strings."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def find_best_match(self, query: str, candidates: list[str]) -> Tuple[Optional[str], float]:
        """Encuentra la mejor coincidencia para una consulta."""
        if not candidates:
            logger.warning("No candidates available for matching")
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        for candidate in candidates:
            score = self.calculate_similarity(query, candidate)
            if score > best_score:
                best_score = score
                best_match = candidate
        
        if best_score < self.threshold:
            logger.info(f"No match found above threshold for query: {query[:50]}...")
            return None, best_score
        
        logger.info(f"Best match found with confidence {best_score:.2f}")
        return best_match, best_score

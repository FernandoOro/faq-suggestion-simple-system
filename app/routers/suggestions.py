"""
Router para el endpoint de sugerencias.
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models import QueryRequest, SuggestionResponse
from app.services import KnowledgeBase, SimilarityService, HistoryService
from app.dependencies import get_knowledge_base, get_similarity_service, get_history_service
from app.config import logger

router = APIRouter(prefix="/suggest", tags=["suggestions"])


@router.post("", response_model=SuggestionResponse)
async def suggest_answer(
    request: QueryRequest,
    kb: KnowledgeBase = Depends(get_knowledge_base),
    similarity: SimilarityService = Depends(get_similarity_service),
    history: HistoryService = Depends(get_history_service)
) -> SuggestionResponse:
    """Sugiere una respuesta basada en la consulta del usuario."""
    logger.info(f"Received suggestion request: {request.query}")
    
    questions = kb.get_all_questions()
    best_match, confidence = similarity.find_best_match(request.query, questions)
    
    if best_match is None:
        logger.warning(f"No suggestion found for query: {request.query}")
        raise HTTPException(
            status_code=404,
            detail="No se encontró ninguna sugerencia similar."
        )
    
    answer = kb.get_answer(best_match)
    
    if answer is None:
        logger.error(f"Answer not found for matched question: {best_match}")
        raise HTTPException(status_code=500, detail="Error interno.")
    
    history.add_entry(request.query, answer, confidence)
    logger.info(f"Suggestion provided with confidence {confidence:.2f}")
    
    return SuggestionResponse(query=request.query, suggestion=answer, confidence=confidence)

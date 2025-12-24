"""
Aplicación principal de FastAPI con gestión de ciclo de vida.
"""
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, API_PREFIX, INITIAL_KNOWLEDGE_FILE, logger
from app.dependencies import get_knowledge_base, get_history_service
from app.routers import suggestions, history, knowledge
from app.models import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager para gestionar el ciclo de vida de la aplicación."""
    logger.info("=== APPLICATION STARTUP ===")
    
    try:
        with open(INITIAL_KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
            knowledge_data = json.load(f)
        
        kb = get_knowledge_base()
        kb.load_knowledge(knowledge_data)
        
        logger.info(f"Successfully loaded {kb.count()} knowledge entries")
        
    except FileNotFoundError:
        logger.error(f"Knowledge file not found: {INITIAL_KNOWLEDGE_FILE}")
        logger.warning("Starting with empty knowledge base")
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in knowledge file: {e}")
        logger.warning("Starting with empty knowledge base")
    
    logger.info("Application startup complete")
    
    yield
    
    logger.info("=== APPLICATION SHUTDOWN ===")


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API RESTful para sugerencias de FAQ basadas en similitud de texto",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restringir en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(suggestions.router, prefix=API_PREFIX)
app.include_router(history.router, prefix=API_PREFIX)
app.include_router(knowledge.router, prefix=API_PREFIX)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health_check() -> HealthResponse:
    """Endpoint de verificación de salud de la aplicación."""
    kb = get_knowledge_base()
    hist = get_history_service()
    
    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        knowledge_entries=kb.count(),
        history_entries=hist.count()
    )


@app.get("/", tags=["root"])
def root():
    """Endpoint raíz con información básica."""
    return {
        "message": f"Welcome to {APP_NAME}",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

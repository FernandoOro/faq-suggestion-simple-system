"""Configuración de fixtures para tests con pytest."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_knowledge_base, get_similarity_service, get_history_service


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def sample_knowledge():
    return {
        "¿Cómo reseteo mi contraseña?": "Para resetear tu contraseña, haz clic en 'Olvidé mi contraseña'.",
        "¿Cómo contacto con soporte?": "Puedes contactarnos en soporte@empresa.com.",
        "¿Cuál es el límite de almacenamiento?": "El plan gratuito incluye 5GB de almacenamiento."
    }


@pytest.fixture(autouse=True)
def reset_services():
    get_knowledge_base.cache_clear()
    get_similarity_service.cache_clear()
    get_history_service.cache_clear()
    yield
    get_knowledge_base.cache_clear()
    get_similarity_service.cache_clear()
    get_history_service.cache_clear()


@pytest.fixture
def populated_knowledge_base(sample_knowledge):
    kb = get_knowledge_base()
    kb.load_knowledge(sample_knowledge)
    return kb

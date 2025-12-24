"""Tests para el endpoint de conocimiento."""
import pytest
from fastapi import status


class TestKnowledgeEndpoint:
    def test_add_knowledge_success(self, test_client, populated_knowledge_base):
        response = test_client.post(
            "/api/v1/knowledge",
            json={"question": "¿Nueva pregunta?", "answer": "Nueva respuesta"}
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_add_knowledge_duplicate(self, test_client, populated_knowledge_base):
        response = test_client.post(
            "/api/v1/knowledge",
            json={"question": "¿Cómo reseteo mi contraseña?", "answer": "Otra respuesta"}
        )
        assert response.status_code == status.HTTP_409_CONFLICT

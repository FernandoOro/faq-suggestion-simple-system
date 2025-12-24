"""Tests para el endpoint de sugerencias."""
import pytest
from fastapi import status


class TestSuggestEndpoint:
    def test_suggest_exact_match(self, test_client, populated_knowledge_base):
        response = test_client.post("/api/v1/suggest", json={"query": "¿Cómo reseteo mi contraseña?"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "suggestion" in data
        assert data["confidence"] > 0.9
    
    def test_suggest_no_match(self, test_client, populated_knowledge_base):
        response = test_client.post("/api/v1/suggest", json={"query": "xyz123 random text"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_suggest_empty_query(self, test_client, populated_knowledge_base):
        response = test_client.post("/api/v1/suggest", json={"query": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

"""Tests para el endpoint de historial."""
import pytest
from fastapi import status


class TestHistoryEndpoint:
    def test_history_empty(self, test_client, populated_knowledge_base):
        response = test_client.get("/api/v1/history")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
    
    def test_history_with_entries(self, test_client, populated_knowledge_base):
        test_client.post("/api/v1/suggest", json={"query": "¿Cómo reseteo mi contraseña?"})
        response = test_client.get("/api/v1/history")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] >= 1

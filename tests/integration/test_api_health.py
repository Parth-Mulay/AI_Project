"""Integration tests for health check and server endpoints."""

import pytest


class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_invalid_route(self, client):
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404


class TestCORS:
    def test_cors_headers_present(self, client):
        response = client.options(
            "/api/v1/meetings",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code in (200, 204)
        assert "access-control-allow-origin" in response.headers

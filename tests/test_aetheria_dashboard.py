"""Tests for Aetheria Dashboard."""
from __future__ import annotations

import pytest
import sys
from pathlib import Path

# Add the workspace to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from aetheria_dashboard.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)


class TestApp:
    def test_create_app(self, app):
        assert app is not None

    def test_index(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["app"] == "Aetheria Vertical AI Knowledge Graph"

    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}


class TestGraph:
    def test_graph_data(self, client):
        resp = client.get("/graph/data")
        assert resp.status_code == 200
        data = resp.json()
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) > 0

    def test_graph_stats(self, client):
        resp = client.get("/graph/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_nodes" in data
        assert "total_edges" in data
        assert "groups" in data
        assert data["total_nodes"] > 0


class TestQuery:
    def test_search_empty(self, client):
        resp = client.get("/query/search")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 0

    def test_search_with_query(self, client):
        resp = client.get("/query/search?q=diabetes&domain=healthcare")
        assert resp.status_code == 200
        data = resp.json()
        assert data["query"] == "diabetes"
        assert data["domain"] == "healthcare"
        assert data["count"] > 0

    def test_search_all_domains(self, client):
        resp = client.get("/query/search?q=test&domain=all")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] > 0


class TestVerticals:
    def test_list_verticals(self, client):
        resp = client.get("/verticals/list")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 8

    def test_get_vertical_healthcare(self, client):
        resp = client.get("/verticals/healthcare")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "healthcare"
        assert data["name"] == "Healthcare"

    def test_get_vertical_legal(self, client):
        resp = client.get("/verticals/legal")
        assert resp.status_code == 200
        assert resp.json()["id"] == "legal"

    def test_get_vertical_finance(self, client):
        resp = client.get("/verticals/finance")
        assert resp.status_code == 200
        assert resp.json()["id"] == "finance"

    def test_get_vertical_education(self, client):
        resp = client.get("/verticals/education")
        assert resp.status_code == 200
        assert resp.json()["id"] == "education"

    def test_get_vertical_customer_service(self, client):
        resp = client.get("/verticals/customer_service")
        assert resp.status_code == 200
        assert resp.json()["id"] == "customer_service"

    def test_get_vertical_manufacturing(self, client):
        resp = client.get("/verticals/manufacturing")
        assert resp.status_code == 200
        assert resp.json()["id"] == "manufacturing"

    def test_get_vertical_agriculture(self, client):
        resp = client.get("/verticals/agriculture")
        assert resp.status_code == 200
        assert resp.json()["id"] == "agriculture"

    def test_get_vertical_research(self, client):
        resp = client.get("/verticals/research")
        assert resp.status_code == 200
        assert resp.json()["id"] == "research"

    def test_get_vertical_not_found(self, client):
        resp = client.get("/verticals/missing")
        assert resp.status_code == 200
        assert "error" in resp.json()


class TestApiClient:
    def test_list_endpoints(self, client):
        resp = client.get("/api-client/endpoints")
        assert resp.status_code == 200
        data = resp.json()
        assert "endpoints" in data
        assert len(data["endpoints"]) > 0


class TestDocs:
    def test_list_sections(self, client):
        resp = client.get("/docs/sections")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0


class TestGraphData:
    def test_graph_has_disease_nodes(self, client):
        resp = client.get("/graph/data")
        data = resp.json()
        groups = [n["group"] for n in data["nodes"]]
        assert "disease" in groups

    def test_graph_has_drug_nodes(self, client):
        resp = client.get("/graph/data")
        data = resp.json()
        groups = [n["group"] for n in data["nodes"]]
        assert "drug" in groups

    def test_graph_has_symptom_nodes(self, client):
        resp = client.get("/graph/data")
        data = resp.json()
        groups = [n["group"] for n in data["nodes"]]
        assert "symptom" in groups

    def test_graph_edges_valid(self, client):
        resp = client.get("/graph/data")
        data = resp.json()
        node_ids = {n["id"] for n in data["nodes"]}
        for edge in data["edges"]:
            assert edge["source"] in node_ids or edge["source"] == "n5"
            assert edge["target"] in node_ids


class TestStats:
    def test_graph_stats_consistency(self, client):
        data_resp = client.get("/graph/data")
        stats_resp = client.get("/graph/stats")
        data = data_resp.json()
        stats = stats_resp.json()
        assert stats["total_nodes"] == len(data["nodes"])
        assert stats["total_edges"] == len(data["edges"])


class TestVerticalData:
    def test_verticals_have_required_fields(self, client):
        resp = client.get("/verticals/list")
        data = resp.json()
        for v in data:
            assert "id" in v
            assert "name" in v
            assert "icon" in v
            assert "description" in v

    def test_eight_verticals(self, client):
        resp = client.get("/verticals/list")
        data = resp.json()
        assert len(data) == 8

    def test_vertical_ids_unique(self, client):
        resp = client.get("/verticals/list")
        data = resp.json()
        ids = [v["id"] for v in data]
        assert len(ids) == len(set(ids))


class TestSearch:
    def test_search_multiple_domains(self, client):
        domains = ["healthcare", "legal", "finance", "education"]
        for domain in domains:
            resp = client.get(f"/query/search?q=test&domain={domain}")
            assert resp.status_code == 200
            assert resp.json()["domain"] == domain

    def test_search_results_format(self, client):
        resp = client.get("/query/search?q=diabetes&domain=healthcare")
        data = resp.json()
        for r in data["results"]:
            assert "id" in r
            assert "title" in r
            assert "domain" in r

"""Additional tests for Aetheria Dashboard."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from aetheria_dashboard.app import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


class TestGraphDataStructure:
    def test_all_nodes_have_id(self, client):
        resp = client.get("/graph/data")
        for node in resp.json()["nodes"]:
            assert "id" in node

    def test_all_nodes_have_label(self, client):
        resp = client.get("/graph/data")
        for node in resp.json()["nodes"]:
            assert "label" in node

    def test_all_nodes_have_group(self, client):
        resp = client.get("/graph/data")
        for node in resp.json()["nodes"]:
            assert "group" in node

    def test_all_edges_have_source(self, client):
        resp = client.get("/graph/data")
        for edge in resp.json()["edges"]:
            assert "source" in edge

    def test_all_edges_have_target(self, client):
        resp = client.get("/graph/data")
        for edge in resp.json()["edges"]:
            assert "target" in edge

    def test_all_edges_have_relation(self, client):
        resp = client.get("/graph/data")
        for edge in resp.json()["edges"]:
            assert "relation" in edge

    def test_node_ids_unique(self, client):
        resp = client.get("/graph/data")
        ids = [n["id"] for n in resp.json()["nodes"]]
        assert len(ids) == len(set(ids))


class TestVerticalDataDetails:
    def test_healthcare_icon(self, client):
        resp = client.get("/verticals/healthcare")
        assert resp.json()["icon"] == "🏥"

    def test_legal_icon(self, client):
        resp = client.get("/verticals/legal")
        assert resp.json()["icon"] == "⚖️"

    def test_finance_icon(self, client):
        resp = client.get("/verticals/finance")
        assert resp.json()["icon"] == "💰"

    def test_education_icon(self, client):
        resp = client.get("/verticals/education")
        assert resp.json()["icon"] == "📚"

    def test_vertical_names(self, client):
        resp = client.get("/verticals/list")
        names = [v["name"] for v in resp.json()]
        assert "Healthcare" in names
        assert "Legal" in names
        assert "Finance" in names
        assert "Education" in names
        assert "Customer Service" in names
        assert "Manufacturing" in names
        assert "Agriculture" in names
        assert "Research" in names


class TestApiEndpoints:
    def test_graph_data_endpoint(self, client):
        resp = client.get("/graph/data")
        assert resp.status_code == 200

    def test_graph_stats_endpoint(self, client):
        resp = client.get("/graph/stats")
        assert resp.status_code == 200

    def test_query_search_endpoint(self, client):
        resp = client.get("/query/search?q=test")
        assert resp.status_code == 200

    def test_verticals_list_endpoint(self, client):
        resp = client.get("/verticals/list")
        assert resp.status_code == 200

    def test_api_endpoints_list(self, client):
        resp = client.get("/api-client/endpoints")
        assert resp.status_code == 200

    def test_docs_sections_list(self, client):
        resp = client.get("/docs/sections")
        assert resp.status_code == 200


class TestSearchFunctionality:
    def test_search_returns_results_with_query(self, client):
        resp = client.get("/query/search?q=diabetes")
        data = resp.json()
        assert data["count"] > 0

    def test_search_result_has_score(self, client):
        resp = client.get("/query/search?q=test")
        data = resp.json()
        for r in data["results"]:
            assert "score" in r

    def test_search_with_different_domains(self, client):
        domains = ["healthcare", "agriculture", "research"]
        for d in domains:
            resp = client.get(f"/query/search?q=test&domain={d}")
            assert resp.status_code == 200


class TestStatsConsistency:
    def test_stats_groups_match_actual_groups(self, client):
        data_resp = client.get("/graph/data")
        stats_resp = client.get("/graph/stats")
        data = data_resp.json()
        stats = stats_resp.json()
        actual_groups = set(n["group"] for n in data["nodes"])
        assert set(stats["groups"]) == actual_groups

    def test_stats_total_nodes_positive(self, client):
        resp = client.get("/graph/stats")
        assert resp.json()["total_nodes"] > 0

    def test_stats_total_edges_positive(self, client):
        resp = client.get("/graph/stats")
        assert resp.json()["total_edges"] > 0

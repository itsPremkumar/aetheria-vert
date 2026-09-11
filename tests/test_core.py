"""Tests for Aetheria Core."""
from __future__ import annotations

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from aetheria.core import (
    Entity,
    Relation,
    Query,
    QueryResult,
    KnowledgeGraph,
    QueryEngine,
    MultiAgentOrchestrator,
    KnowledgeReasoner,
    VerticalPlugin,
)


# ─── Entity Tests ──────────────────────────────────────────────────────────────

class TestEntity:
    def test_create_entity(self):
        entity = Entity(id="1", name="test", entity_type="disease", vertical="healthcare")
        assert entity.id == "1"
        assert entity.name == "test"
        assert entity.entity_type == "disease"
        assert entity.vertical == "healthcare"

    def test_to_dict(self):
        entity = Entity(id="1", name="test", entity_type="disease", vertical="healthcare", description="Test entity")
        d = entity.to_dict()
        assert d["id"] == "1"
        assert d["name"] == "test"
        assert d["description"] == "Test entity"

    def test_from_dict(self):
        d = {"id": "1", "name": "test", "entity_type": "disease", "vertical": "healthcare", "description": "", "metadata": {}}
        entity = Entity.from_dict(d)
        assert entity.id == "1"
        assert entity.name == "test"


# ─── Relation Tests ────────────────────────────────────────────────────────────

class TestRelation:
    def test_create_relation(self):
        rel = Relation(id="1", source_id="s1", target_id="t1", relation_type="treats", vertical="healthcare")
        assert rel.id == "1"
        assert rel.source_id == "s1"
        assert rel.target_id == "t1"
        assert rel.relation_type == "treats"

    def test_to_dict(self):
        rel = Relation(id="1", source_id="s1", target_id="t1", relation_type="treats", vertical="healthcare", confidence=0.8)
        d = rel.to_dict()
        assert d["confidence"] == 0.8

    def test_from_dict(self):
        d = {"id": "1", "source_id": "s1", "target_id": "t1", "relation_type": "treats", "vertical": "healthcare", "confidence": 0.5}
        rel = Relation.from_dict(d)
        assert rel.source_id == "s1"


# ─── KnowledgeGraph Tests ──────────────────────────────────────────────────────

class TestKnowledgeGraph:
    def test_add_and_get_entities(self):
        graph = KnowledgeGraph()
        entity = Entity(id="1", name="test", entity_type="disease", vertical="healthcare")
        graph.add_entity(entity)
        assert len(graph.get_entities()) == 1

    def test_get_by_vertical(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="test1", entity_type="disease", vertical="healthcare"))
        graph.add_entity(Entity(id="2", name="test2", entity_type="disease", vertical="legal"))
        assert len(graph.get_entities(vertical="healthcare")) == 1
        assert len(graph.get_entities(vertical="legal")) == 1

    def test_get_by_type(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="test1", entity_type="disease", vertical="healthcare"))
        graph.add_entity(Entity(id="2", name="test2", entity_type="drug", vertical="healthcare"))
        assert len(graph.get_entities(entity_type="disease")) == 1

    def test_search(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="diabetes", entity_type="disease", vertical="healthcare"))
        results = graph.search("diabetes")
        assert len(results) == 1

    def test_stats(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="test1", entity_type="disease", vertical="healthcare"))
        graph.add_entity(Entity(id="2", name="test2", entity_type="drug", vertical="healthcare"))
        stats = graph.stats()
        assert "healthcare/disease" in stats
        assert "healthcare/drug" in stats


# ─── QueryEngine Tests ─────────────────────────────────────────────────────────

class TestQueryEngine:
    def test_query(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="diabetes", entity_type="disease", vertical="healthcare"))
        engine = QueryEngine(graph)
        result = engine.query("diabetes")
        assert isinstance(result, QueryResult)
        assert result.confidence > 0

    def test_query_no_results(self):
        graph = KnowledgeGraph()
        engine = QueryEngine(graph)
        result = engine.query("nonexistent")
        assert result.confidence == 0


# ─── MultiAgentOrchestrator Tests ──────────────────────────────────────────────

class TestMultiAgentOrchestrator:
    def test_register_plugin(self):
        orch = MultiAgentOrchestrator()
        plugin = VerticalPlugin("test")
        orch.register_plugin(plugin)
        assert orch.get_plugin("test") is not None

    def test_list_plugins(self):
        orch = MultiAgentOrchestrator()
        orch.register_plugin(VerticalPlugin("test1"))
        orch.register_plugin(VerticalPlugin("test2"))
        assert len(orch.list_plugins()) == 2

    def test_process(self):
        orch = MultiAgentOrchestrator()
        plugin = VerticalPlugin("test")
        plugin.register_pattern("item", [r"\b(test_item)\b"])
        orch.register_plugin(plugin)
        result = orch.process("This is a test_item")
        assert "test" in result

    def test_cross_vertical_query(self):
        orch = MultiAgentOrchestrator()
        plugin = VerticalPlugin("test")
        plugin.register_pattern("item", [r"\b(test_item)\b"])
        orch.register_plugin(plugin)
        results = orch.cross_vertical_query("This is a test_item")
        assert isinstance(results, dict)


# ─── KnowledgeReasoner Tests ───────────────────────────────────────────────────

class TestKnowledgeReasoner:
    def test_infer(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="a", entity_type="disease", vertical="healthcare"))
        graph.add_entity(Entity(id="2", name="b", entity_type="drug", vertical="healthcare"))
        graph.add_relation(Relation(id="r1", source_id="1", target_id="2", relation_type="treats", vertical="healthcare"))
        reasoner = KnowledgeReasoner(graph)
        relations = reasoner.infer("1")
        assert len(relations) >= 1

    def test_find_path(self):
        graph = KnowledgeGraph()
        graph.add_entity(Entity(id="1", name="a", entity_type="disease", vertical="healthcare"))
        graph.add_entity(Entity(id="2", name="b", entity_type="drug", vertical="healthcare"))
        graph.add_relation(Relation(id="r1", source_id="1", target_id="2", relation_type="treats", vertical="healthcare"))
        reasoner = KnowledgeReasoner(graph)
        path = reasoner.find_path("1", "2")
        assert path is not None
        assert "1" in path
        assert "2" in path


# ─── VerticalPlugin Tests ──────────────────────────────────────────────────────

class TestVerticalPlugin:
    def test_create_plugin(self):
        plugin = VerticalPlugin("test", "Test plugin")
        assert plugin.name == "test"
        assert plugin.description == "Test plugin"

    def test_register_pattern(self):
        plugin = VerticalPlugin("test")
        plugin.register_pattern("item", [r"\b(test)\b"])
        entities = plugin.extract_entities("This is a test")
        assert len(entities) == 1
        assert entities[0].name == "test"

    def test_register_relation(self):
        plugin = VerticalPlugin("test")
        plugin.register_pattern("source", [r"\b(source)\b"])
        plugin.register_pattern("target", [r"\b(target)\b"])
        plugin.register_relation("source", "relates_to", "target")
        entities = plugin.extract_entities("source and target")
        relations = plugin.extract_relations(entities, "source and target")
        assert len(relations) >= 1

    def test_reason(self):
        plugin = VerticalPlugin("test")
        result = plugin.reason([], "query")
        assert isinstance(result, str)

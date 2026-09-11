"""Aetheria Core — Query Engine, Orchestrator, Plugin Base, Reasoner."""
from __future__ import annotations

import uuid
import time
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Protocol
from datetime import datetime, timezone


# ─── Data Models ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Entity:
    """A knowledge entity."""
    id: str
    name: str
    entity_type: str
    vertical: str
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "entity_type": self.entity_type,
            "vertical": self.vertical,
            "description": self.description,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Entity:
        return cls(**d)


@dataclass(frozen=True)
class Relation:
    """A relation between entities."""
    id: str
    source_id: str
    target_id: str
    relation_type: str
    vertical: str
    confidence: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "vertical": self.vertical,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Relation:
        return cls(**d)


@dataclass
class Query:
    """A query to the knowledge graph."""
    id: str
    text: str
    vertical: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    """Result of a query."""
    query_id: str
    entities: list[Entity]
    relations: list[Relation]
    answer: str
    confidence: float
    duration: float
    vertical: str | None = None


# ─── Entity Extractor Protocol ─────────────────────────────────────────────────

class EntityExtractor(Protocol):
    """Protocol for entity extractors."""

    def extract(self, text: str) -> list[Entity]: ...

    @property
    def vertical(self) -> str: ...


# ─── Relation Extractor Protocol ───────────────────────────────────────────────

class RelationExtractor(Protocol):
    """Protocol for relation extractors."""

    def extract(self, entities: list[Entity], text: str) -> list[Relation]: ...

    @property
    def vertical(self) -> str: ...


# ─── Plugin Base ───────────────────────────────────────────────────────────────

class VerticalPlugin:
    """Base class for vertical plugins."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self._patterns: dict[str, list[str]] = {}
        self._relations: dict[str, str] = {}

    @property
    def vertical(self) -> str:
        return self.name

    def register_pattern(self, entity_type: str, patterns: list[str]) -> None:
        """Register regex patterns for an entity type."""
        self._patterns[entity_type] = patterns

    def register_relation(self, source_type: str, relation_type: str, target_type: str) -> None:
        """Register a relation type between entity types."""
        self._relations[f"{source_type}->{target_type}"] = relation_type

    def extract_entities(self, text: str) -> list[Entity]:
        """Extract entities from text using registered patterns."""
        entities: list[Entity] = []
        seen: set[str] = set()
        for entity_type, patterns in self._patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    name = match.group(0).lower().strip()
                    if name not in seen:
                        seen.add(name)
                        entities.append(Entity(
                            id=str(uuid.uuid4()),
                            name=name,
                            entity_type=entity_type,
                            vertical=self.name,
                        ))
        return entities

    def extract_relations(self, entities: list[Entity], text: str) -> list[Relation]:
        """Extract relations between entities."""
        relations: list[Relation] = []
        text_lower = text.lower()
        for i, src in enumerate(entities):
            for tgt in entities[i + 1:]:
                key = f"{src.entity_type}->{tgt.entity_type}"
                if key in self._relations:
                    if src.name in text_lower and tgt.name in text_lower:
                        relations.append(Relation(
                            id=str(uuid.uuid4()),
                            source_id=src.id,
                            target_id=tgt.id,
                            relation_type=self._relations[key],
                            vertical=self.name,
                            confidence=0.5,
                        ))
        return relations

    def reason(self, entities: list[Entity], query: str) -> str:
        """Generate a reasoning-based answer."""
        return f"Analysis of {len(entities)} entities from {self.name} vertical."


# ─── Knowledge Graph ───────────────────────────────────────────────────────────

class KnowledgeGraph:
    """In-memory knowledge graph."""

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}
        self._relations: list[Relation] = []

    def add_entity(self, entity: Entity) -> None:
        self._entities[entity.id] = entity

    def add_relation(self, relation: Relation) -> None:
        self._relations.append(relation)

    def get_entities(self, vertical: str | None = None, entity_type: str | None = None) -> list[Entity]:
        entities = list(self._entities.values())
        if vertical:
            entities = [e for e in entities if e.vertical == vertical]
        if entity_type:
            entities = [e for e in entities if e.entity_type == entity_type]
        return entities

    def get_relations(self, vertical: str | None = None) -> list[Relation]:
        if vertical:
            return [r for r in self._relations if r.vertical == vertical]
        return list(self._relations)

    def search(self, query: str, vertical: str | None = None) -> list[Entity]:
        """Search entities by name or description."""
        q = query.lower()
        results: list[Entity] = []
        for entity in self._entities.values():
            if vertical and entity.vertical != vertical:
                continue
            if q in entity.name.lower() or q in entity.description.lower():
                results.append(entity)
        return results

    def stats(self) -> dict[str, int]:
        stats: dict[str, int] = {}
        for entity in self._entities.values():
            key = f"{entity.vertical}/{entity.entity_type}"
            stats[key] = stats.get(key, 0) + 1
        return stats


# ─── Query Engine ──────────────────────────────────────────────────────────────

class QueryEngine:
    """Query engine for the knowledge graph."""

    def __init__(self, graph: KnowledgeGraph) -> None:
        self._graph = graph

    def query(self, text: str, vertical: str | None = None) -> QueryResult:
        """Execute a query against the knowledge graph."""
        start = time.perf_counter()
        query = Query(id=str(uuid.uuid4()), text=text, vertical=vertical)
        entities = self._graph.search(text, vertical)
        relations = self._graph.get_relations(vertical)
        relevant_relations = [
            r for r in relations
            if r.source_id in {e.id for e in entities} or r.target_id in {e.id for e in entities}
        ]
        answer = f"Found {len(entities)} entities and {len(relevant_relations)} relations."
        duration = time.perf_counter() - start
        return QueryResult(
            query_id=query.id,
            entities=entities,
            relations=relevant_relations,
            answer=answer,
            confidence=0.8 if entities else 0.0,
            duration=duration,
            vertical=vertical,
        )


# ─── Multi-Agent Orchestrator ─────────────────────────────────────────────────

class MultiAgentOrchestrator:
    """Orchestrate queries across multiple verticals."""

    def __init__(self) -> None:
        self._plugins: dict[str, VerticalPlugin] = {}
        self._graph = KnowledgeGraph()
        self._engine = QueryEngine(self._graph)

    def register_plugin(self, plugin: VerticalPlugin) -> None:
        """Register a vertical plugin."""
        self._plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> VerticalPlugin | None:
        return self._plugins.get(name)

    def list_plugins(self) -> list[VerticalPlugin]:
        return list(self._plugins.values())

    def process(self, text: str, vertical: str | None = None) -> dict[str, Any]:
        """Process text through the appropriate vertical plugin."""
        results: dict[str, Any] = {}
        plugins = [self._plugins[vertical]] if vertical and vertical in self._plugins else self._plugins.values()
        for plugin in plugins:
            entities = plugin.extract_entities(text)
            relations = plugin.extract_relations(entities, text)
            for entity in entities:
                self._graph.add_entity(entity)
            for relation in relations:
                self._graph.add_relation(relation)
            results[plugin.name] = {
                "entities": [e.to_dict() for e in entities],
                "relations": [r.to_dict() for r in relations],
            }
        return results

    def query(self, text: str, vertical: str | None = None) -> QueryResult:
        """Query the knowledge graph."""
        return self._engine.query(text, vertical)

    def cross_vertical_query(self, text: str) -> dict[str, QueryResult]:
        """Query across all verticals."""
        results: dict[str, QueryResult] = {}
        for name, plugin in self._plugins.items():
            entities = plugin.extract_entities(text)
            if entities:
                results[name] = self._engine.query(text, name)
        return results

    def get_stats(self) -> dict[str, int]:
        return self._graph.stats()


# ─── Knowledge Reasoner ───────────────────────────────────────────────────────

class KnowledgeReasoner:
    """Knowledge reasoner for inference."""

    def __init__(self, graph: KnowledgeGraph) -> None:
        self._graph = graph

    def infer(self, entity_id: str, depth: int = 2) -> list[Relation]:
        """Infer relations for an entity up to a given depth."""
        visited: set[str] = set()
        relations: list[Relation] = []
        self._infer_recursive(entity_id, depth, visited, relations)
        return relations

    def _infer_recursive(self, entity_id: str, depth: int, visited: set[str], relations: list[Relation]) -> None:
        if depth <= 0 or entity_id in visited:
            return
        visited.add(entity_id)
        for relation in self._graph.get_relations():
            if relation.source_id == entity_id or relation.target_id == entity_id:
                relations.append(relation)
                next_id = relation.target_id if relation.source_id == entity_id else relation.source_id
                self._infer_recursive(next_id, depth - 1, visited, relations)

    def find_path(self, source_id: str, target_id: str, max_depth: int = 4) -> list[str] | None:
        """Find a path between two entities."""
        visited: set[str] = set()
        path: list[str] = []
        if self._dfs(source_id, target_id, max_depth, visited, path):
            return path
        return None

    def _dfs(self, current: str, target: str, depth: int, visited: set[str], path: list[str]) -> bool:
        if depth <= 0 or current in visited:
            return False
        visited.add(current)
        path.append(current)
        if current == target:
            return True
        for relation in self._graph.get_relations():
            next_id: str | None = None
            if relation.source_id == current:
                next_id = relation.target_id
            elif relation.target_id == current:
                next_id = relation.source_id
            if next_id and self._dfs(next_id, target, depth - 1, visited, path):
                return True
        path.pop()
        return False

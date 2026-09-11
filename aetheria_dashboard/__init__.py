"""Aetheria Vertical AI Knowledge Graph — Web Dashboard.

Real-time vertical KG visualization, query interface, domain selector,
interactive knowledge graph explorer, REST API client, and documentation.
"""
from __future__ import annotations

__version__ = "1.0.0"

from .app import create_app

__all__ = ["create_app"]

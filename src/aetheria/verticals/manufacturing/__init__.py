"""Manufacturing Vertical Plugin."""
from __future__ import annotations
from ..core import VerticalPlugin


class ManufacturingPlugin(VerticalPlugin):
    """Manufacturing domain plugin."""

    def __init__(self) -> None:
        super().__init__("manufacturing", "Manufacturing domain — processes, equipment, quality, supply chain")
        self.register_pattern("process", [
            r"\b(assembly|fabrication|molding|casting|machining|welding|printing|coating)\b",
            r"\b(heat treatment|surface treatment|inspection|testing|packaging|shipping)\b",
        ])
        self.register_pattern("equipment", [
            r"\b(CNC|lathe|mill|press|drill|grinder|robot|conveyor|furnace|extruder)\b",
        ])
        self.register_pattern("quality", [
            r"\b(ISO 9001|Six Sigma|lean manufacturing|total quality management|Kaizen)\b",
            r"\b(defect rate|first pass yield|scrap rate|rework|non-conformance)\b",
        ])
        self.register_pattern("supply_chain", [
            r"\b(supplier|vendor|warehouse|inventory|procurement|logistics|distribution)\b",
            r"\b(just-in-time|lean supply|demand planning|procurement|sourcing)\b",
        ])
        self.register_pattern("safety", [
            r"\b(PPE|hazard|risk assessment|incident|near miss|safety audit|OSHA)\b",
        ])
        self.register_relation("process", "uses", "equipment")
        self.register_relation("quality", "monitors", "process")
        self.register_relation("supply_chain", "provides", "equipment")

    def reason(self, entities: list, query: str) -> str:
        processes = [e for e in entities if e.entity_type == "process"]
        equipment = [e for e in entities if e.entity_type == "equipment"]
        quality = [e for e in entities if e.entity_type == "quality"]
        parts = []
        if processes:
            parts.append(f"Manufacturing processes: {', '.join(p.name for p in processes)}")
        if equipment:
            parts.append(f"Equipment: {', '.join(e.name for e in equipment)}")
        if quality:
            parts.append(f"Quality standards: {', '.join(q.name for q in quality)}")
        if not parts:
            return "No specific manufacturing entities identified."
        return ". ".join(parts) + "."

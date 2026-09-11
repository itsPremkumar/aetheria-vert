"""Agriculture Vertical Plugin."""
from __future__ import annotations
from ..core import VerticalPlugin


class AgriculturePlugin(VerticalPlugin):
    """Agriculture domain plugin."""

    def __init__(self) -> None:
        super().__init__("agriculture", "Agriculture domain — crops, soil, pests, nutrients, climate")
        self.register_pattern("crop", [
            r"\b(wheat|corn|rice|soybean|potato|tomato|cotton|sugarcane|barley|oat)\b",
            r"\b(apple|grape|citrus|banana|mango|pineberry|strawberry|blueberry)\b",
        ])
        self.register_pattern("soil", [
            r"\b(clay|sandy|silty|loam|peat|chalk|silt|gravel|alluvial|laterite)\b",
            r"\b(topsoil|subsoil|bedrock|humus|compost|mulch|fertilizer|manure)\b",
        ])
        self.register_pattern("pest", [
            r"\b(aphid|caterpillar|beetle|locust|nematode|mite|thrips|whitefly)\b",
            r"\b(fungus|bacteria|virus|weed|mold|mildew|rot|blight)\b",
        ])
        self.register_pattern("nutrient", [
            r"\b(nitrogen|phosphorus|potassium|calcium|magnesium|sulfur|iron|zinc)\b",
            r"\b(NPK|micronutrient|macronutrient|organic matter|pH|EC)\b",
        ])
        self.register_pattern("climate", [
            r"\b(temperature|humidity|rainfall|sunlight|wind|frost|drought|flood)\b",
            r"\b(tropical|temperate|arid|continental|mediterranean|monsoon|polar)\b",
        ])
        self.register_relation("crop", "grows_in", "soil")
        self.register_relation("crop", "requires", "nutrient")
        self.register_relation("pest", "attacks", "crop")
        self.register_relation("climate", "affects", "crop")

    def reason(self, entities: list, query: str) -> str:
        crops = [e for e in entities if e.entity_type == "crop"]
        soils = [e for e in entities if e.entity_type == "soil"]
        pests = [e for e in entities if e.entity_type == "pest"]
        nutrients = [e for e in entities if e.entity_type == "nutrient"]
        climate = [e for e in entities if e.entity_type == "climate"]
        parts = []
        if crops:
            parts.append(f"Crops: {', '.join(c.name for c in crops)}")
        if soils:
            parts.append(f"Soil types: {', '.join(s.name for s in soils)}")
        if pests:
            parts.append(f"Pests/diseases: {', '.join(p.name for p in pests)}")
        if nutrients:
            parts.append(f"Nutrients: {', '.join(n.name for n in nutrients)}")
        if climate:
            parts.append(f"Climate factors: {', '.join(c.name for c in climate)}")
        if not parts:
            return "No specific agriculture entities identified."
        return ". ".join(parts) + "."

"""Knowledge graph explorer router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

# Sample graph data for visualization
SAMPLE_GRAPH = {
    "nodes": [
        {"id": "n1", "label": "Diabetes", "group": "disease"},
        {"id": "n2", "label": "Metformin", "group": "drug"},
        {"id": "n3", "label": "Insulin", "group": "drug"},
        {"id": "n4", "label": "Hypertension", "group": "disease"},
        {"id": "n5", "label": "Lisinopril", "group": "drug"},
        {"id": "n6", "label": "Fever", "group": "symptom"},
        {"id": "n7", "label": "Cough", "group": "symptom"},
    ],
    "edges": [
        {"source": "n2", "target": "n1", "relation": "treats"},
        {"source": "n3", "target": "n1", "relation": "treats"},
        {"source": "n5", "target": "n4", "relation": "treats"},
        {"source": "n6", "target": "n1", "relation": "symptom_of"},
        {"source": "n7", "target": "n4", "relation": "symptom_of"},
    ]
}

@router.get("/", response_class=HTMLResponse)
async def graph_page(request: Request):
    from fastapi.templating import Jinja2Templates
    from pathlib import Path
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
    return templates.TemplateResponse("graph.html", {"request": request})

@router.get("/data")
async def graph_data():
    return SAMPLE_GRAPH

@router.get("/stats")
async def graph_stats():
    return {
        "total_nodes": len(SAMPLE_GRAPH["nodes"]),
        "total_edges": len(SAMPLE_GRAPH["edges"]),
        "groups": list(set(n["group"] for n in SAMPLE_GRAPH["nodes"])),
    }

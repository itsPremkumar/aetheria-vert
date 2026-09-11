"""Vertical domains router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

VERTICALS = [
    {"id": "healthcare", "name": "Healthcare", "icon": "🏥", "description": "Medical KG with drug interactions, diagnosis support"},
    {"id": "legal", "name": "Legal", "icon": "⚖️", "description": "Legal entities, case law, contracts"},
    {"id": "finance", "name": "Finance", "icon": "💰", "description": "Financial instruments, markets, risk analysis"},
    {"id": "education", "name": "Education", "icon": "📚", "description": "Learning paths, concepts, quizzes"},
    {"id": "customer_service", "name": "Customer Service", "icon": "🎧", "description": "Support knowledge base, ticket routing"},
    {"id": "manufacturing", "name": "Manufacturing", "icon": "🏭", "description": "Supply chain, processes, quality control"},
    {"id": "agriculture", "name": "Agriculture", "icon": "🌾", "description": "Crops, soil, weather, pest management"},
    {"id": "research", "name": "Research", "icon": "🔬", "description": "Academic papers, citations, discoveries"},
]

@router.get("/", response_class=HTMLResponse)
async def verticals_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
    return templates.TemplateResponse("verticals.html", {"request": request})

@router.get("/list")
async def list_verticals():
    return VERTICALS

@router.get("/{vertical_id}")
async def get_vertical(vertical_id: str):
    for v in VERTICALS:
        if v["id"] == vertical_id:
            return v
    return {"error": "Vertical not found"}

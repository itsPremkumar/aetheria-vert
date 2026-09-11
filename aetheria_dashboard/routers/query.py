"""Query interface router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

DOMAINS = ["all", "healthcare", "legal", "finance", "education", "customer_service", "manufacturing", "agriculture", "research"]

@router.get("/", response_class=HTMLResponse)
async def query_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
    return templates.TemplateResponse("query.html", {"request": request})

@router.get("/search")
async def search(q: str = "", domain: str = "all"):
    """Search the knowledge graph."""
    results = []
    if q:
        results = [
            {"id": "r1", "title": f"Result for: {q}", "domain": domain, "score": 0.95},
            {"id": "r2", "title": f"Related: {q}", "domain": domain, "score": 0.87},
        ]
    return {"query": q, "domain": domain, "results": results, "count": len(results)}

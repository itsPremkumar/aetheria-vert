"""REST API client router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

ENDPOINTS = [
    {"path": "/graph/data", "method": "GET", "description": "Get graph data"},
    {"path": "/graph/stats", "method": "GET", "description": "Get graph statistics"},
    {"path": "/query/search", "method": "GET", "description": "Search KG"},
    {"path": "/verticals/list", "method": "GET", "description": "List verticals"},
    {"path": "/health", "method": "GET", "description": "Health check"},
]

@router.get("/", response_class=HTMLResponse)
async def api_client_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
    return templates.TemplateResponse("api_client.html", {"request": request})

@router.get("/endpoints")
async def list_endpoints():
    return {"endpoints": ENDPOINTS}

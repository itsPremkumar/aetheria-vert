"""Documentation router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

DOCS_SECTIONS = [
    {"id": "intro", "title": "Introduction", "content": "Welcome to Aetheria - the Vertical AI Knowledge Graph Platform."},
    {"id": "quickstart", "title": "Quick Start", "content": "Get started in 5 minutes with the dashboard."},
    {"id": "api", "title": "API Reference", "content": "REST API documentation for all endpoints."},
    {"id": "plugins", "title": "Plugins", "content": "How to add new vertical domains."},
    {"id": "deployment", "title": "Deployment", "content": "Deploy to production with Docker or bare metal."},
]

@router.get("/", response_class=HTMLResponse)
async def docs_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
    return templates.TemplateResponse("docs.html", {"request": request})

@router.get("/sections")
async def list_sections():
    return DOCS_SECTIONS

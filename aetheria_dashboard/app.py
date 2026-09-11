"""FastAPI application factory."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .routers import graph, query, verticals, api_client, docs

BASE_DIR = Path(__file__).parent

def create_app() -> FastAPI:
    app = FastAPI(
        title="Aetheria Vertical AI Knowledge Graph",
        description="Real-time vertical KG visualization and query interface",
        version="1.0.0",
    )

    # Mount static files
    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Include routers
    app.include_router(graph.router, prefix="/graph", tags=["graph"])
    app.include_router(query.router, prefix="/query", tags=["query"])
    app.include_router(verticals.router, prefix="/verticals", tags=["verticals"])
    app.include_router(api_client.router, prefix="/api-client", tags=["api-client"])
    app.include_router(docs.router, prefix="/docs", tags=["docs"])

    @app.get("/")
    async def index():
        return {"app": "Aetheria Vertical AI Knowledge Graph", "version": "1.0.0", "status": "running"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app

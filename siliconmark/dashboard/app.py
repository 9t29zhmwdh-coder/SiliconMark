"""FastAPI dashboard server: serves the HTML UI and exposes /api/results."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from siliconmark.exporters.json_exporter import load_results

_STATIC = Path(__file__).parent / "static"


def create_app(results_dir: Path) -> FastAPI:
    app = FastAPI(title="SiliconMark Dashboard", docs_url=None, redoc_url=None)

    @app.get("/")
    def index():
        return FileResponse(_STATIC / "index.html")

    @app.get("/api/results")
    def get_results():
        items = load_results(results_dir)
        return JSONResponse([r.model_dump(mode="json") for r in items])

    app.mount("/static", StaticFiles(directory=str(_STATIC)), name="static")
    return app

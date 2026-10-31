"""Local FastAPI reasoner: compile → OWL-RL close → SPARQL execute."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rdflib import Graph

from ask.compile_nl import compile as compile_question
from ask.intents import execute
from ask.json_to_rdf import DEFAULT_JSON, load_graph
from ask.reason import close

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_FILES = {
    "favicon.svg": "image/svg+xml",
    "favicon.ico": "image/x-icon",
    "apple-touch-icon.png": "image/png",
    "apple-touch-icon-precomposed.png": "image/png",
}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_closed: Graph | None = None


def _closed_graph() -> Graph:
    global _closed
    if _closed is None:
        _closed = close(load_graph())
    return _closed


class AskBody(BaseModel):
    q: str


@app.get("/")
def viewer() -> FileResponse:
    return FileResponse(ROOT / "index.html", media_type="text/html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(f"/{DEFAULT_JSON.name}")
def graph_json() -> FileResponse:
    return FileResponse(DEFAULT_JSON, media_type="application/json")


@app.get("/{filename}")
def public_file(filename: str) -> FileResponse:
    media = PUBLIC_FILES.get(filename)
    if media is None:
        raise HTTPException(status_code=404, detail="Not Found")
    path = ROOT / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(path, media_type=media)


@app.post("/ask")
def ask(body: AskBody):
    ir = compile_question(body.q)
    if "error" in ir:
        return JSONResponse(
            status_code=422,
            content={"error": ir["error"], "candidates": ir["candidates"]},
        )
    hops = execute({"intent": ir["intent"], "seed": ir["seed"]}, _closed_graph())
    body: dict[str, object] = {
        "ir": {"intent": ir["intent"], "seed": ir["seed"]},
        "hops": hops,
    }
    if not hops:
        body["note"] = "No stored hops for this question."
    return body


app.mount("/vendor", StaticFiles(directory=ROOT / "vendor"), name="vendor")

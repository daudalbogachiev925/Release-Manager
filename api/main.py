from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.release import create_release, mark_released
from src.storage import ReleaseStorage
from src.changelog import render_changelog
from src.version import Version, classify_changes

app = FastAPI(title="Release Manager")
storage = ReleaseStorage()

class Commit(BaseModel):
    type: str
    message: str
    hash: str
    scope: str = ""
    breaking: bool = False

class CreateRelease(BaseModel):
    version: str
    planned_date: str
    features: List[str] = []
    bugfixes: List[str] = []

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/releases")
def list_releases():
    return storage.list_all()

@app.post("/releases")
def create(data: CreateRelease):
    r = create_release(data.version, data.planned_date,
                       data.features, data.bugfixes)
    storage.save(r)
    return r.to_dict()

@app.post("/releases/{version}/release")
def mark_release(version: str):
    r = storage.load(version)
    if not r:
        raise HTTPException(404, "Release not found")
    mark_released(r)
    storage.save(r)
    return r.to_dict()

@app.post("/changelog")
def changelog(version: str, commits: List[Commit]):
    bump = classify_changes([c.dict() for c in commits])
    content = render_changelog(version, [c.dict() for c in commits])
    return {"bump": bump.value, "changelog": content}

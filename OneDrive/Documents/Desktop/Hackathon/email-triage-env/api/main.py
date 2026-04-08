import json
from typing import Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from env.environment import EmailTriageEnvironment, TASK_REGISTRY
from env.models import Action, EnvironmentState, Observation, StepResult

app = FastAPI(title="Email Triage OpenEnv", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_envs: Dict[str, EmailTriageEnvironment] = {}


def _get_env(session_id: str, task_id: Optional[str] = None) -> EmailTriageEnvironment:
    if session_id not in _envs:
        tid = task_id or list(TASK_REGISTRY.keys())[0]
        _envs[session_id] = EmailTriageEnvironment(task_id=tid)
    return _envs[session_id]


class ResetRequest(BaseModel):
    task_id: str = "task_easy_classify"
    session_id: str = "default"
    
    class Config:
        extra = "ignore"


class StepRequest(BaseModel):
    action: Action
    session_id: str = "default"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "email-triage-env"}


@app.get("/tasks")
def list_tasks():
    return {"tasks": [
        {"id": "task_easy_classify", "name": "Email Classification", "difficulty": "easy", "max_steps": 10},
        {"id": "task_medium_triage", "name": "Email Triage", "difficulty": "medium", "max_steps": 10},
        {"id": "task_hard_full_triage", "name": "Full Triage + Response", "difficulty": "hard", "max_steps": 10},
    ]}


@app.post("/reset", response_model=Observation)
def reset():
    """Reset environment - no parameters, always uses defaults"""
    task_id = "task_easy_classify"
    session_id = "default"
    
    if task_id not in TASK_REGISTRY:
        raise HTTPException(status_code=400, detail=f"Unknown task_id '{task_id}'")
    _envs[session_id] = EmailTriageEnvironment(task_id=task_id)
    return _envs[session_id].reset()


@app.post("/step", response_model=StepResult)
async def step(request: Request):
    """Step environment - requires action in body"""
    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Step request body required with action")
    
    if not isinstance(body, dict) or "action" not in body:
        raise HTTPException(status_code=400, detail="Step request body required with action")
    
    session_id = body.get("session_id", "default")
    env = _get_env(session_id)
    return env.step(Action(**body["action"]))


@app.get("/state", response_model=EnvironmentState)
def state(session_id: str = Query(default="default")):
    return _get_env(session_id).state()


@app.get("/")
def root():
    return {"name": "Email Triage OpenEnv", "version": "1.0.0", "docs": "/docs"}
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EmailItem(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    timestamp: str
    category: Optional[str] = None
    priority: Optional[str] = None


class Observation(BaseModel):
    task_id: str = Field(..., description="Current task identifier")
    task_description: str = Field(..., description="Natural language task description")
    emails: List[EmailItem] = Field(..., description="Emails available to process")
    inbox_size: int = Field(..., description="Total emails in inbox")
    step_number: int = Field(..., description="Current step in episode")
    max_steps: int = Field(..., description="Maximum steps allowed")
    context: Dict[str, Any] = Field(default_factory=dict)
    available_actions: List[str] = Field(..., description="List of valid action types")


class Action(BaseModel):
    action_type: str = Field(..., description="One of: classify, prioritize, route, respond, archive, flag, skip")
    email_id: str = Field(..., description="Target email ID")
    classification: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)
    routing_department: Optional[str] = Field(None)
    response_draft: Optional[str] = Field(None)
    reasoning: Optional[str] = Field(None)


class Reward(BaseModel):
    total: float = Field(..., description="Total reward 0.0-1.0")
    classification_score: float = Field(0.0)
    priority_score: float = Field(0.0)
    routing_score: float = Field(0.0)
    response_score: float = Field(0.0)
    penalty: float = Field(0.0)
    message: str = Field("")


class StepResult(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class EnvironmentState(BaseModel):
    task_id: str
    step_number: int
    max_steps: int
    total_reward: float
    emails_processed: int
    emails_remaining: int
    episode_done: bool
    task_scores: Dict[str, float] = Field(default_factory=dict)
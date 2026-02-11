from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentRequest(BaseModel):
    goal: str


class PlanStep(BaseModel):
    id: int
    action: str
    details: str
    tool: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    goal: str
    plan: List[PlanStep]
    result: List[Dict[str, Any]]

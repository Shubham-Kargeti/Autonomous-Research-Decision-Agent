from pydantic import BaseModel
from typing import Any, List

class AgentRequest(BaseModel):
    goal: str


class AgentResponse(BaseModel):
    goal: str
    plan: List[Any]
    result: List[Any]

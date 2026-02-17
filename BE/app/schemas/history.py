from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from uuid import UUID


class AgentRunHistory(BaseModel):
    id: UUID
    goal: str
    plan: List[Dict[str, Any]]
    result: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True  

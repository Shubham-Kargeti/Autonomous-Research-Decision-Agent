from fastapi import APIRouter
from app.schemas import AgentRequest, AgentResponse
from app.agent.agent import run_agent

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/run", response_model=AgentResponse)
def run_agent_endpoint(request: AgentRequest):
    """
    Run the agent with a structured goal.
    """

    return run_agent(request.goal)

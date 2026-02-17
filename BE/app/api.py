from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.agent import AgentRequest, AgentResponse
from app.schemas.history import AgentRunHistory
from app.agent.agent import run_agent
from app.dependencies import get_current_user, get_db
from app.db.models import AgentRun, User

router = APIRouter(prefix="/agent", tags=["agent"])


# ==========================================================
# RUN AGENT
# ==========================================================
@router.post("/run", response_model=AgentResponse)
async def run_agent_endpoint(
    request: AgentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Run LLM agent
    response = run_agent(request.goal)

    # Save run in DB
    new_run = AgentRun(
        user_id=current_user.id,
        goal=request.goal,
        plan=response.plan,
        result=response.result,
    )

    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)

    return response


# ==========================================================
# GET USER HISTORY
# ==========================================================
@router.get("/history", response_model=list[AgentRunHistory])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AgentRun)
        .where(AgentRun.user_id == current_user.id)
        .order_by(AgentRun.created_at.desc())
    )

    runs = result.scalars().all()
    return runs

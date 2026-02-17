from app.agent.planner import create_plan
from app.agent.executor import execute_plan
from app.schemas.agent import AgentResponse

def run_agent(goal: str) -> AgentResponse:
    print(f"[AGENT] Goal received: {goal}")

    plan = create_plan(goal)

    execution_results = execute_plan(plan)

    return AgentResponse(
        goal=goal,
        plan=plan,
        result=execution_results
    )

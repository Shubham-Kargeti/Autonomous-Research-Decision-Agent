from app.agent.tools.web_search import web_search

def execute_plan(plan):
    execution_results = []

    print(f"[EXECUTOR] Executing {len(plan)} steps")

    for step in plan:
        print(f"[EXECUTOR] Step {step['id']}: {step['action']}")

        tool = step.get("tool")
        tool_output = None

        if tool == "web_search":
            query = step.get("tool_input", {}).get("query")
            tool_output = web_search(query)

        execution_results.append({
            "step_id": step["id"],
            "action": step["action"],
            "status": "completed",
            "tool_used": tool,
            "tool_output": tool_output
        })

    return execution_results

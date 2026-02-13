from app.agent.tools.web_search import web_search
from app.agent.planner import revise_plan, critic_step
from app.agent.llm import call_llm


def execute_plan(plan):
    execution_results = []
    working_memory = []
    remaining_steps = plan.copy()

    MAX_RETRIES = 1

    print("[EXECUTOR] Starting adaptive execution")

    while remaining_steps:
        step = remaining_steps.pop(0)

        print(f"[EXECUTOR] Step {step['id']}: {step['action']}")

        tool = step.get("tool")
        retry_count = 0
        tool_output = None
        critic_result = {"status": "approved", "reason": "No critic needed"}

        while True:
            tool_output = None

            # ---- TOOL EXECUTION ----
            if tool == "web_search":
                query = step.get("tool_input", {}).get("query")
                tool_output = web_search(query)

            # ---- REASONING EXECUTION ----
            elif tool is None:
                reasoning_prompt = f"""
You are executing the following task step:

Action: {step['action']}
Details: {step['details']}

Use the working memory below if relevant:

{working_memory}

Provide a clear and structured result.
"""

                tool_output = call_llm(
                    "You are a strategic task execution assistant.",
                    reasoning_prompt
                )

            # ---- CRITIC EVALUATION ----
            critic_result = critic_step(step, tool_output)

            if critic_result.get("status") == "approved":
                break

            if retry_count >= MAX_RETRIES:
                print(
                    f"[CRITIC] Max retries reached for step {step['id']}. "
                    "Proceeding with current result."
                )
                break

            print(
                f"[CRITIC] Retrying step {step['id']} - "
                f"Reason: {critic_result.get('reason')}"
            )

            retry_count += 1

        # ---- STORE MEMORY ONLY IF APPROVED ----
        if tool_output and critic_result.get("status") == "approved":
            working_memory.append({
                "step_id": step["id"],
                "action": step["action"],
                "tool_output": tool_output
            })

        execution_results.append({
            "step_id": step["id"],
            "action": step["action"],
            "status": critic_result.get("status"),
            "critic_reason": critic_result.get("reason"),
            "tool_used": tool,
            "tool_output": tool_output,
            "retries": retry_count
        })

        # ---- REPLAN ----
        if remaining_steps:
            remaining_steps = revise_plan(
                original_plan=plan,
                working_memory=working_memory,
                remaining_steps=remaining_steps
            )

    return execution_results

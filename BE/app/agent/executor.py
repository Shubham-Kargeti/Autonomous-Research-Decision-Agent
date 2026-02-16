from app.agent.tools.web_search import web_search
# from app.agent.planner import revise_plan, critic_step   # ⬅️ Disabled to reduce LLM calls
# from app.agent.llm import call_llm                       # ⬅️ Disabled reasoning LLM calls


def execute_plan(plan):
    execution_results = []
    working_memory = []
    remaining_steps = plan.copy()

    print("[EXECUTOR] Running in BASIC MODE (LLM-minimized)")

    while remaining_steps:
        step = remaining_steps.pop(0)

        print(f"[EXECUTOR] Step {step['id']}: {step['action']}")

        tool = step.get("tool")
        tool_output = None

        # ----------------------------
        # TOOL EXECUTION (Allowed)
        # ----------------------------
        if tool == "web_search":
            query = step.get("tool_input", {}).get("query")
            tool_output = web_search(query)

        # ----------------------------
        # REASONING EXECUTION DISABLED
        # ----------------------------
        # elif tool is None:
        #     reasoning_prompt = f"""
        #     You are executing the following task step:
        #
        #     Action: {step['action']}
        #     Details: {step['details']}
        #
        #     Use the working memory below if relevant:
        #
        #     {working_memory}
        #
        #     Provide a clear and structured result.
        #     """
        #
        #     tool_output = call_llm(
        #         "You are a strategic task execution assistant.",
        #         reasoning_prompt
        #     )

        # Instead of LLM reasoning, just return structured placeholder
        if tool is None:
            tool_output = f"Step '{step['action']}' acknowledged. (Basic mode execution)"

        # ----------------------------
        # CRITIC DISABLED
        # ----------------------------
        # critic_result = critic_step(step, tool_output)
        critic_result = {"status": "approved", "reason": "basic mode"}

        # ----------------------------
        # MEMORY STORAGE
        # ----------------------------
        if tool_output:
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
            "retries": 0
        })

        # ----------------------------
        # REPLANNER DISABLED
        # ----------------------------
        # if remaining_steps:
        #     remaining_steps = revise_plan(
        #         original_plan=plan,
        #         working_memory=working_memory,
        #         remaining_steps=remaining_steps
        #     )

    print("[EXECUTOR] Basic execution completed.")
    return execution_results

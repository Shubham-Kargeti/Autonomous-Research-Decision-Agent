import json
from app.agent.llm import call_llm

SYSTEM_PROMPT = """
You are a task planning AI.

Return ONLY valid JSON.
No markdown.
No explanations.

Available tools:
- web_search (requires: query)
- none (for reasoning-only steps)

IMPORTANT:
If the goal involves:
- Real-world positions
- Institutions
- Organizations
- Religious seats
- Government roles
- Locations
- Current procedures
- Eligibility criteria
- Legal or formal processes

Then you MUST use tool="web_search"
to verify accurate and up-to-date information.

Only skip web_search if the step is purely reasoning-based.

Schema:
{
  "steps": [
    {
      "id": number,
      "action": string,
      "details": string,
      "tool": string | null,
      "tool_input": object | null
    }
  ]
}
"""



# ==========================================================
# BASIC MODE: Only 1 LLM Call (Planner Only)
# ==========================================================

def create_plan(goal: str):
    user_prompt = f"Goal: {goal}"

    raw = call_llm(SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json.loads(raw)
        return parsed["steps"]
    except Exception:
        print("[PLANNER] Invalid JSON detected.")

        # --------------------------------------------------
        # SELF-REPAIR DISABLED (removes extra LLM call)
        # --------------------------------------------------
        # repair_prompt = f"""
        # The following output is invalid JSON.
        # Fix it and return ONLY valid JSON in the required schema.
        #
        # Output:
        # {raw}
        # """
        #
        # repaired = call_llm(SYSTEM_PROMPT, repair_prompt)
        #
        # try:
        #     parsed = json.loads(repaired)
        #     return parsed["steps"]
        # except Exception:
        #     raise ValueError("Planner failed after repair attempt.")

        raise ValueError("Planner returned invalid JSON.")


# ==========================================================
# REPLANNER (DISABLED FOR BASIC MODE)
# ==========================================================

def revise_plan(original_plan, working_memory, remaining_steps):
    """
    Re-plan remaining steps based on memory.
    Currently disabled to reduce LLM calls.
    """

    print("[REPLANNER] Disabled in basic mode. Returning original remaining steps.")

    # --------------------------------------------------
    # FULL MODE (Future - Uncomment When Needed)
    # --------------------------------------------------
    # revision_prompt = f"""
    # You are revising a task plan.
    #
    # Original plan:
    # {json.dumps(original_plan, indent=2)}
    #
    # Working memory:
    # {json.dumps(working_memory, indent=2)}
    #
    # Remaining steps:
    # {json.dumps(remaining_steps, indent=2)}
    #
    # Modify remaining steps if needed.
    # Return ONLY valid JSON:
    #
    # {{
    #   "steps": [...]
    # }}
    # """
    #
    # raw = call_llm("You are a planning assistant.", revision_prompt)
    #
    # try:
    #     parsed = json.loads(raw)
    #     return parsed["steps"]
    # except Exception:
    #     print("[REPLANNER] Failed. Keeping original remaining steps.")
    #     return remaining_steps

    return remaining_steps


# ==========================================================
# CRITIC (DISABLED FOR BASIC MODE)
# ==========================================================

def critic_step(step, tool_output):
    """
    Evaluate execution step.
    Currently disabled to reduce LLM calls.
    """

    print("[CRITIC] Disabled in basic mode. Auto-approving step.")

    # --------------------------------------------------
    # FULL MODE (Future - Uncomment When Needed)
    # --------------------------------------------------
    # critic_prompt = f"""
    # Evaluate this step execution.
    #
    # Step:
    # Action: {step['action']}
    # Details: {step['details']}
    #
    # Output:
    # {tool_output}
    #
    # Return ONLY valid JSON:
    #
    # {{
    #   "status": "approved" OR "retry",
    #   "reason": "short explanation"
    # }}
    # """
    #
    # raw = call_llm("You are a strict execution evaluator.", critic_prompt)
    #
    # try:
    #     parsed = json.loads(raw)
    #     return parsed
    # except Exception:
    #     return {"status": "approved", "reason": "Critic parsing failed"}

    return {"status": "approved", "reason": "basic mode"}

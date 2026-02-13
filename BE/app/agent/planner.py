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

If a step requires external information, assign tool="web_search"
and include tool_input with required fields.

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

def create_plan(goal: str):
    user_prompt = f"Goal: {goal}"

    raw = call_llm(SYSTEM_PROMPT, user_prompt)

    try:
        parsed = json.loads(raw)
        return parsed["steps"]
    except Exception:
        print("[PLANNER] Invalid JSON detected. Attempting self-repair...")

        repair_prompt = f"""
The following output is invalid JSON.
Fix it and return ONLY valid JSON in the required schema.

Output:
{raw}
"""

        repaired = call_llm(SYSTEM_PROMPT, repair_prompt)

        try:
            parsed = json.loads(repaired)
            return parsed["steps"]
        except Exception:
            raise ValueError("Planner failed to produce valid JSON after repair attempt.")


def revise_plan(original_plan, working_memory, remaining_steps):
    """
    Re-plan remaining steps based on memory.
    """

    revision_prompt = f"""
You are revising a task plan.

Original plan:
{json.dumps(original_plan, indent=2)}

Working memory (completed steps + tool outputs):
{json.dumps(working_memory, indent=2)}

Remaining steps:
{json.dumps(remaining_steps, indent=2)}

If memory suggests improvements, modify remaining steps.
Keep the same schema.
Return ONLY valid JSON:

{{
  "steps": [...]
}}
"""

    raw = call_llm("You are a planning assistant.", revision_prompt)

    try:
        parsed = json.loads(raw)
        return parsed["steps"]
    except Exception:
        print("[REPLANNER] Failed to revise plan. Keeping original remaining steps.")
        return remaining_steps


def critic_step(step, tool_output):
    critic_prompt = f"""
Evaluate this step execution.

Step:
Action: {step['action']}
Details: {step['details']}

Output:
{tool_output}

Return ONLY valid JSON:

{{
  "status": "approved" OR "retry",
  "reason": "short explanation"
}}

No explanations.
No markdown.
No extra text.
"""

    raw = call_llm("You are a strict execution evaluator.", critic_prompt)

    print("\n[CRITIC RAW OUTPUT]\n", raw, "\n")

    try:
        parsed = json.loads(raw)
        return parsed
    except Exception as e:
        print("[CRITIC ERROR]", e)
        return {"status": "approved", "reason": "Critic parsing failed"}

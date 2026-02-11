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

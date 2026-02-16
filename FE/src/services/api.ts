export async function runAgent(goal: string) {
  const response = await fetch("http://localhost:8000/agent/run", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ goal })
  });

  if (!response.ok) {
    throw new Error("Failed to run agent");
  }

  return response.json();
}

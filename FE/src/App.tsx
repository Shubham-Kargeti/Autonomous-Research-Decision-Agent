import { useState } from "react";
import { runAgent } from "./services/api";
import GoalInput from "./components/GoalInput";
import PlanView from "./components/PlanView";
import ResultView from "./components/ResultView";
import type { Step, ExecutionResult } from "./types";
import "./styles.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<Step[]>([]);
  const [result, setResult] = useState<ExecutionResult[]>([]);

  const handleSubmit = async (goal: string) => {
    setLoading(true);
    try {
      const data = await runAgent(goal);
      setPlan(data.plan);
      setResult(data.result);
    } catch (err) {
      console.error(err);
      alert("Error running agent");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Agentic AI System</h1>
      <GoalInput onSubmit={handleSubmit} loading={loading} />
      <PlanView plan={plan} />
      <ResultView result={result} />
    </div>
  );
}

export default App;

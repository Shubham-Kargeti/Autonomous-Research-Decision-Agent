import { useState } from "react";

interface Props {
  onSubmit: (goal: string) => void;
  loading: boolean;
}

export default function GoalInput({ onSubmit, loading }: Props) {
  const [goal, setGoal] = useState("");

  return (
    <div className="goal-box">
      <input
        type="text"
        placeholder="Enter your goal..."
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      />
      <button onClick={() => onSubmit(goal)} disabled={loading}>
        {loading ? "Running..." : "Run Agent"}
      </button>
    </div>
  );
}

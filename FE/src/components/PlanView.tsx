import type { Step } from "../types";    

interface Props {
  plan: Step[];
}

export default function PlanView({ plan }: Props) {
  if (!plan.length) return null;

  return (
    <div className="section">
      <h2>Generated Plan</h2>

      {plan.map((step) => (
        <div key={step.id} className="card">
          <strong>
            Step {step.id}: {step.action}
          </strong>

          <p>{step.details}</p>

          {step.tool && (
            <div style={{ marginTop: "8px" }}>
              <span
                style={{
                  background: "#222",
                  color: "#fff",
                  padding: "4px 8px",
                  borderRadius: "6px",
                  fontSize: "12px",
                }}
              >
                Tool: {step.tool}
              </span>

              {step.tool_input && (
                <pre
                  style={{
                    background: "#111",
                    padding: "10px",
                    borderRadius: "6px",
                    marginTop: "6px",
                    overflowX: "auto",
                  }}
                >
                  {JSON.stringify(step.tool_input, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

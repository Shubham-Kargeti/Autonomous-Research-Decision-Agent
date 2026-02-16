import { useState } from "react";
import type { ExecutionResult } from "../types";

interface Props {
  result: ExecutionResult[];
}

export default function ResultView({ result }: Props) {
  if (!result.length) return null;

  return (
    <div className="section">
      <h2>Execution Result</h2>

      {result.map((r) => (
        <ResultCard key={r.step_id} result={r} />
      ))}
    </div>
  );
}

function ResultCard({ result }: { result: ExecutionResult }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="card">
      <strong>{result.action}</strong>

      <p>
        Status:{" "}
        <span
          style={{
            color: result.status === "approved" ? "limegreen" : "orange",
          }}
        >
          {result.status}
        </span>
      </p>

      <button
        onClick={() => setOpen(!open)}
        style={{
          marginTop: "6px",
          padding: "4px 8px",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        {open ? "Hide Details" : "View Details"}
      </button>

      {open && (
        <div
          style={{
            marginTop: "10px",
            background: "#111",
            padding: "10px",
            borderRadius: "6px",
          }}
        >
          <p>
            <strong>Critic Reason:</strong> {result.critic_reason}
          </p>

          <p>
            <strong>Retries:</strong> {result.retries}
          </p>

          {result.tool_used && (
            <>
              <p>
                <strong>Tool Used:</strong> {result.tool_used}
              </p>

              <pre
                style={{
                  background: "#000",
                  padding: "8px",
                  borderRadius: "6px",
                  overflowX: "auto",
                }}
              >
                {typeof result.tool_output === "string"
                  ? result.tool_output
                  : JSON.stringify(result.tool_output, null, 2)}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}

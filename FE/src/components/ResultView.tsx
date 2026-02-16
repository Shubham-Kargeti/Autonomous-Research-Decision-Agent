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

  const isWebSearch =
    result.tool_used === "web_search" &&
    Array.isArray(result.tool_output);

  const statusColor =
    result.status === "approved" ? "#16a34a" : "#f59e0b";

  return (
    <div
      className="card"
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "16px",
        background: "#ffffff",
      }}
    >
      {/* Step Title */}
      <h3 style={{ marginBottom: "8px" }}>{result.action}</h3>

      {/* Status Badge */}
      <span
        style={{
          background: statusColor,
          color: "#fff",
          padding: "4px 10px",
          borderRadius: "999px",
          fontSize: "12px",
          fontWeight: 500,
        }}
      >
        {result.status.toUpperCase()}
      </span>

      {/* Non-tool simple output */}
      {!isWebSearch && result.tool_output && (
        <p style={{ marginTop: "12px", color: "#374151" }}>
          {result.tool_output}
        </p>
      )}

      {/* Toggle Button */}
      <button
        onClick={() => setOpen(!open)}
        style={{
          marginTop: "12px",
          padding: "6px 12px",
          borderRadius: "8px",
          cursor: "pointer",
          border: "1px solid #d1d5db",
          background: "#f9fafb",
        }}
      >
        {open ? "Hide Details" : "View Details"}
      </button>

      {/* Expandable Section */}
      {open && (
        <div
          style={{
            marginTop: "16px",
            padding: "14px",
            background: "#f9fafb",
            borderRadius: "10px",
            border: "1px solid #e5e7eb",
          }}
        >
          <p style={{ marginBottom: "6px" }}>
            <strong>Critic:</strong> {result.critic_reason}
          </p>

          <p style={{ marginBottom: "12px" }}>
            <strong>Retries:</strong> {result.retries}
          </p>

          {/* Web Search Results */}
          {isWebSearch && (
            <>
              <h4 style={{ marginBottom: "10px" }}>
                🔍 Web Search Results
              </h4>

              {result.tool_output.map((item: any, index: number) => (
                <div
                  key={index}
                  style={{
                    marginBottom: "12px",
                    padding: "12px",
                    background: "#ffffff",
                    borderRadius: "8px",
                    border: "1px solid #e5e7eb",
                  }}
                >
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      color: "#2563eb",
                      fontWeight: 600,
                      textDecoration: "none",
                    }}
                  >
                    {item.title}
                  </a>

                  <p
                    style={{
                      fontSize: "14px",
                      marginTop: "6px",
                      color: "#4b5563",
                    }}
                  >
                    {item.content}
                  </p>
                </div>
              ))}
            </>
          )}

          {/* Fallback JSON */}
          {!isWebSearch &&
            typeof result.tool_output === "object" && (
              <pre
                style={{
                  background: "#111827",
                  color: "#f9fafb",
                  padding: "10px",
                  borderRadius: "8px",
                  overflowX: "auto",
                  fontSize: "12px",
                }}
              >
                {JSON.stringify(result.tool_output, null, 2)}
              </pre>
            )}
        </div>
      )}
    </div>
  );
}

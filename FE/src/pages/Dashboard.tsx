import { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../pages/styles/Dashboard.css";
import LoadingOverlay from "../components/LoadingOverlay";
import ErrorModal from "../components/ErrorModal";

interface AgentRun {
  id: string;
  goal: string;
  plan: any[];
  result: any[];
  created_at: string;
}

interface Props {
  activeTab: string;
}

function Dashboard({ activeTab }: Props) {
  const { user, getAccessTokenSilently } = useAuth0();

  const [goal, setGoal] = useState("");
  const [output, setOutput] = useState<any[]>([]);
  const [history, setHistory] = useState<AgentRun[]>([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // ==============================
  // Run Agent
  // ==============================
  const runAgent = async () => {
    if (!goal.trim()) return;

    setLoading(true);
    setOutput([]);

    try {
      const token = await getAccessTokenSilently();

      const response = await fetch(`${API_BASE_URL}/agent/run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ goal }),
      });

      if (!response.ok) {
        throw new Error("Backend Error");
      }

      const data = await response.json();
      setOutput(data.result);
      setGoal("");
      fetchHistory();
    } catch (err) {
      console.error(err);

      const jokes = [
        "Our AI spilled coffee on its neural network ☕🤖",
        "The AI is recalibrating its brain cells 🧠⚡",
        "The robots are on a tea break 🍵",
        "The AI tried to Google itself and panicked 😅",
        "Neural network temporarily disconnected from reality 🔌",
      ];

      const randomJoke =
        jokes[Math.floor(Math.random() * jokes.length)];

      setError(randomJoke);
    }

    setLoading(false);
  };

  // ==============================
  // Fetch History
  // ==============================
  const fetchHistory = async () => {
    setHistoryLoading(true);

    try {
      const token = await getAccessTokenSilently();

      const response = await fetch(`${API_BASE_URL}/agent/history`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch history");
      }

      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error(err);
    }

    setHistoryLoading(false);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <>
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h2>Welcome, {user?.name}</h2>
          <p className="subtitle">
            {activeTab === "agent"
              ? "Run your autonomous AI agent"
              : "Your previous executions"}
          </p>
        </div>

        {/* ============================= */}
        {/* AGENT SECTION */}
        {/* ============================= */}
        {activeTab === "agent" && (
          <div className="agent-section">
            <div className="agent-card">
              <textarea
                placeholder="Enter your research goal (e.g., Study plan for MTech, Market research on EV batteries...)"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
              />

              <button onClick={runAgent} disabled={loading}>
                {loading ? "Running Agent..." : "Run Agent"}
              </button>
            </div>

            <div className="output-section">
              {!loading && output.length === 0 && (
                <div className="empty-state">
                  No results yet. Run the agent to see output.
                </div>
              )}

              {!loading &&
                output.map((step, index) => (
                  <div key={index} className="output-card">
                    <div className="step-header">
                      <span className="step-number">
                        Step {step.step_id}
                      </span>
                      <span className={`status ${step.status}`}>
                        {step.status}
                      </span>
                    </div>

                    <p className="step-action">{step.action}</p>

                    {step.tool_used && (
                      <div className="tool-info">
                        🔧 Tool Used: {step.tool_used}
                      </div>
                    )}
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* ============================= */}
        {/* HISTORY SECTION */}
        {/* ============================= */}
        {activeTab === "history" && (
          <div className="history-section">
            {historyLoading && (
              <p className="loading-text">Loading history...</p>
            )}

            {!historyLoading && history.length === 0 && (
              <div className="empty-state">
                No history available yet.
              </div>
            )}

            {!historyLoading &&
              history.map((item) => (
                <div key={item.id} className="history-card">
                  <div className="history-header">
                    <h4>{item.goal}</h4>
                    <span>
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>

                  <div className="history-meta">
                    {item.result?.length || 0} steps executed
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>

      {/* FULL SCREEN LOADING OVERLAY */}
      {loading && (
        <LoadingOverlay message="Agent is thinking..." />
      )}

      {/* ERROR MODAL */}
      {error && (
        <ErrorModal
          message={error}
          onRetry={() => {
            setError(null);
            runAgent();
          }}
          onClose={() => setError(null)}
        />
      )}
    </>
  );
}

export default Dashboard;

import "../components/styles/Sidebar.css";

interface SidebarProps {
  active: string;
  onChange: (tab: string) => void;
}

function Sidebar({ active, onChange }: SidebarProps) {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <span>⚡</span>
        <h2>AI Agent</h2>
      </div>

      <div className="sidebar-menu">
        <div
          className={`sidebar-item ${active === "agent" ? "active" : ""}`}
          onClick={() => onChange("agent")}
        >
          🤖 Agent
        </div>

        <div
          className={`sidebar-item ${active === "history" ? "active" : ""}`}
          onClick={() => onChange("history")}
        >
          🕒 History
        </div>
      </div>

      <div className="sidebar-footer">
        <small>AI Agent Platform © 2026</small>
      </div>
    </div>
  );
}

export default Sidebar;

import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import "../layout/styles/AppLayout.css";
import Dashboard from "../pages/Dashboard";

function AppLayout() {
  const [activeTab, setActiveTab] = useState("agent");

  return (
    <div className="layout">
      <Sidebar active={activeTab} onChange={setActiveTab} />

      <div className="main-content">
        <Topbar />

        <div className="content-area">
          <Dashboard activeTab={activeTab} />
        </div>
      </div>
    </div>
  );
}

export default AppLayout;

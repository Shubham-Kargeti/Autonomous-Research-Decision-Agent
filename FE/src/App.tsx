import { Routes, Route } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import HomePage from "./pages/HomePage";
import AppLayout from "./layout/AppLayout";

function App() {
  const { isAuthenticated } = useAuth0();

  return (
    <Routes>
      {/* Public Route */}
      <Route path="/" element={<HomePage />} />

      {/* Protected Dashboard Layout */}
      {isAuthenticated && (
        <Route path="/dashboard" element={<AppLayout />} />
      )}
    </Routes>
  );
}

export default App;

import "./styles/HomePage.css";
import { useAuth0 } from "@auth0/auth0-react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const {
    loginWithRedirect,
    logout,
    //user,
    isAuthenticated,
    isLoading,
  } = useAuth0();

  const navigate = useNavigate();

  // Redirect to dashboard after login
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  if (isLoading) return <div className="loading">Loading...</div>;

  return (
    <div className="home-container">
      <div className="navbar">
        <div className="logo">AI Agent</div>

        <div>
          {!isAuthenticated ? (
            <button
              className="btn primary"
              onClick={() =>
                loginWithRedirect({
                  appState: { returnTo: "/dashboard" },
                })
              }
            >
              SignUp / Login
            </button>
          ) : (
            <button
              className="btn secondary"
              onClick={() =>
                logout({
                  logoutParams: {
                    returnTo: window.location.origin,
                  },
                })
              }
            >
              Logout
            </button>
          )}
        </div>
      </div>

      <div className="hero-section">
        <h1>Autonomous AI Research Agent</h1>
        <p>
          Plan. Think. Execute.
          <br />
          Let your AI agent break complex goals into intelligent actions.
        </p>

        {!isAuthenticated && (
          <button
            className="btn primary large"
            onClick={() =>
              loginWithRedirect({
                appState: { returnTo: "/dashboard" },
              })
            }
          >
            Get Started
          </button>
        )}
      </div>

      <footer className="footer">
        <p>© 2026 AI Agent Platform</p>
      </footer>
    </div>
  );
}

export default HomePage;

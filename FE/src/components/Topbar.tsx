import { useAuth0 } from "@auth0/auth0-react";
import "../components/styles/Topbar.css";

function Topbar() {
  const { user, logout } = useAuth0();

  return (
    <div className="topbar">
      <div className="topbar-left">
        <h3>Dashboard</h3>
      </div>

      <div className="topbar-right">
        <div className="user-info">
          <img
            src={user?.picture}
            alt="avatar"
            className="avatar"
          />
          <div>
            <div className="user-name">{user?.name}</div>
            <div className="user-email">{user?.email}</div>
          </div>
        </div>

        <button
          className="logout-btn"
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
      </div>
    </div>
  );
}

export default Topbar;

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import NotesManager from "./components/NotesManager";
import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("access"));

  const handleLogout = () => {
    localStorage.removeItem("access");
    setToken(null);
  };

  return (
    <Router>
      <div>
        <h1>Notes App</h1>
        {token && (
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        )}

        <Routes>
          <Route
            path="/"
            element={
              token ? (
                <NotesManager token={token} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route path="/login" element={<Login setToken={setToken} />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

import { useState } from "react";
import { register } from "../api";
import { useNavigate } from "react-router-dom";
import "../assets/css/Auth.css";

export default function Register() {
  const [data, setData] = useState({ email: "", name: "", password: "" });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await register(data);
      alert(res.message || "Registered");
      navigate("/login");
    } catch (error) {
      alert("Registration failed");
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit}>
        <h2>Register</h2>
        <input
          placeholder="Name"
          onChange={(e) => setData({ ...data, name: e.target.value })}
        />
        <input
          placeholder="Email"
          onChange={(e) => setData({ ...data, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setData({ ...data, password: e.target.value })}
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

import axios from "axios";

const API_BASE = "http://localhost:8000/api";

// Create an axios instance
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// LOGIN
export async function login(email, password) {
  const response = await api.post("/user/login/", { email, password });
  return response.data;
}

// REGISTER
export async function register(data) {
  const response = await api.post("/user/register/", data);
  return response.data;
}

// GET NOTES
export async function getNotes(token) {
  const response = await api.get("/user/notes/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}

// CREATE NOTE
export async function createNote(token, note) {
  const response = await api.post("/user/notes/", note, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}

// UPDATE NOTE
export async function updateNote(token, id, note) {
  const response = await api.put(`/user/notes/${id}/`, note, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}

// DELETE NOTE
export async function deleteNote(token, id) {
  const response = await api.delete(`/user/notes/${id}/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
}

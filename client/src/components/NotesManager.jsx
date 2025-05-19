import { useState, useEffect } from "react";
import { getNotes, createNote, updateNote, deleteNote } from "../api";
import "../assets/css/Notes.css";

export default function NotesManager() {
  const [notes, setNotes] = useState([]);
  const [formData, setFormData] = useState({ title: "", content: "" });
  const [editingId, setEditingId] = useState(null);
  const token = localStorage.getItem("access");

  useEffect(() => {
    (async () => {
      if (!token) return;
      const data = await getNotes(token);
      setNotes(Array.isArray(data) ? data : []);
    })();
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        const updated = await updateNote(token, editingId, formData);
        setNotes(notes.map((n) => (n.id === editingId ? updated : n)));
      } else {
        const newNote = await createNote(token, formData);
        setNotes([...notes, newNote]);
      }
      setFormData({ title: "", content: "" });
      setEditingId(null);
    } catch (err) {
      alert("Failed to save note");
    }
  };

  const handleEdit = (note) => {
    setFormData({ title: note.title, content: note.content });
    setEditingId(note.id);
  };

  const handleDelete = async (id) => {
    await deleteNote(token, id);
    setNotes(notes.filter((n) => n.id !== id));
    if (editingId === id) {
      setFormData({ title: "", content: "" });
      setEditingId(null);
    }
  };

  return (
    <div className="notes-container">
      <h2>{editingId ? "Edit Note" : "Create Note"}</h2>
      <form onSubmit={handleSubmit} className="notes-form">
        <input
          placeholder="Title"
          value={formData.title}
          onChange={(e) =>
            setFormData({ ...formData, title: e.target.value })
          }
        />
        <textarea
          placeholder="Content"
          value={formData.content}
          onChange={(e) =>
            setFormData({ ...formData, content: e.target.value })
          }
        />
        <button type="submit">{editingId ? "Update" : "Create"}</button>
      </form>

      <h2>Your Notes</h2>
      {notes.map((note) => (
        <div className="note-card" key={note.id}>
          <strong>{note.title}</strong>
          <p>{note.content}</p>
          <button onClick={() => handleEdit(note)}>Edit</button>
          <button onClick={() => handleDelete(note.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

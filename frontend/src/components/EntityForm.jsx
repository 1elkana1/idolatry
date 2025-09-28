import { useState } from "react";

export default function EntityForm({ onCreated }) {
  const [form, setForm] = useState({ name: "", patron_id: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch(`${import.meta.env.VITE_API_URL}/entity`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setForm({ name: "", patron_id: "" });
    onCreated();
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
      <input
        type="text"
        name="name"
        placeholder="Entity name"
        value={form.name}
        onChange={handleChange}
        className="border p-2"
        required
      />
      <input
        type="text"
        name="patron_id"
        placeholder="Patron ID (optional)"
        value={form.patron_id}
        onChange={handleChange}
        className="border p-2"
      />
      <button type="submit" className="bg-green-500 text-white px-4 py-2">
        Add Entity
      </button>
    </form>
  );
}

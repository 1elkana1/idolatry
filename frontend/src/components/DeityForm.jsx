import { useState } from "react";

export default function DeityForm({ onCreated }) {
  const [form, setForm] = useState({ name: "", domain: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch(`${import.meta.env.VITE_API_URL}/deity`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setForm({ name: "", domain: "" });
    onCreated(); // refresh state in App
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
      <input
        type="text"
        name="name"
        placeholder="Deity name"
        value={form.name}
        onChange={handleChange}
        className="border p-2"
        required
      />
      <input
        type="text"
        name="domain"
        placeholder="Domain"
        value={form.domain}
        onChange={handleChange}
        className="border p-2"
        required
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2">
        Add Deity
      </button>
    </form>
  );
}

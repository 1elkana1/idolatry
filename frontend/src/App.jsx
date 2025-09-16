import { useState, useEffect } from "react";

function App() {
  const [state, setState] = useState(null);
  const [newDeity, setNewDeity] = useState({ name: "", domain: "" });
  const [newEntity, setNewEntity] = useState("");

  // fetch state from backend
  const fetchState = async () => {
    const res = await fetch("http://127.0.0.1:8000/state");
    const data = await res.json();
    setState(data);
  };
    
  // useEffect = on mount (initial fetch)
  useEffect(() => {
    fetchState();
  }, []);

  // POST deity
  const createDeity = async (e) => {
    e.preventDefault(); // stop the browser from refreshing the page after form submission (default form behavior)
    await fetch("http://127.0.0.1:8000/deity", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newDeity),
    });
    setNewDeity({ name: "", domain: "" }); // clear fields
    fetchState(); // refresh state
  };

  // POST entity
  const createEntity = async (e) => {
    e.preventDefault();
    await fetch("http://127.0.0.1:8000/entity", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newEntity }),
    });
    setNewEntity("");
    fetchState();
  };

  // handle form input changes
  const handleDeityChange = (e) => {
    const { name, value } = e.target;
    setNewDeity((prev) => ({ ...prev, [name]: value }));
  };

  // after all the above js logic, return this jsx (mix of html and js) to be rendered
  // className => config tailwind css classes
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Idolatry Demo</h1>

      {/* Form for deity */}
      <form onSubmit={createDeity} className="mb-4">
        <input
          type="text"
          name="name"
          placeholder="Deity name"
          value={newDeity.name}
          onChange={handleDeityChange}
          className="border p-1 mr-2"
          required
        />
        <input
          type="text"
          name="domain"
          placeholder="Domain"
          value={newDeity.domain}
          onChange={handleDeityChange}
          className="border p-1 mr-2"
          required
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2">
          Add Deity
        </button>
      </form>

      {/* Form for entity */}
      <form onSubmit={createEntity} className="mb-4">
        <input
          type="text"
          value={newEntity}
          onChange={(e) => setNewEntity(e.target.value)}
          placeholder="Entity name"
          className="border p-2 mr-2"
        />
        <button type="submit" className="bg-green-500 text-white px-4 py-2">
          Add Entity
        </button>
      </form>

      {/* Show current state */}
      <pre className="bg-gray-100 p-4 rounded">
        {state ? JSON.stringify(state, null, 2) : "Loading..."}
      </pre>
    </div>
  );
}

export default App;

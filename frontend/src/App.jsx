import { useState, useEffect } from "react";
import DeityForm from "./components/DeityForm";
import EntityForm from "./components/EntityForm";
import EntitiesList from "./components/EntitiesList";
import DeitiesList from "./components/DeitiesList";

function App() {
  const [state, setState] = useState(null);

  const fetchState = async () => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/state`);
    const data = await res.json();
    setState(data);
  };

  useEffect(() => {
    fetchState();
  }, []);

  if (!state) return <p className="p-4">Loading...</p>;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-center">Idolatry Demo</h1>

      {/* Centered forms */}
      <div className="flex flex-col md:flex-col justify-center items-center">
        <DeityForm onCreated={fetchState} />
        <EntityForm onCreated={fetchState} />
      </div>

      {/* Lists side by side */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="border rounded-lg shadow p-4 bg-white flex flex-col">
          <EntitiesList 
            entities={state.entities} 
            fetchState={fetchState} 
          />
        </div>
        <div className="border rounded-lg shadow p-4 bg-white flex flex-col">
          <DeitiesList deities={state.deities} />
        </div>
      </div>
    </div>
  );
}

export default App;
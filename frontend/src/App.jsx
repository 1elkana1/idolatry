import React, { useState, useEffect } from "react";

function App() {
  const [state, setState] = useState({ entities: [], deities: [] });
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [selectedDeity, setSelectedDeity] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/state")
      .then((res) => res.json())
      .then((data) => setState(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">Idolatry Game</h1>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Entities Panel */}
        <div className="md:w-1/2 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Entities</h2>
          {state.entities.length > 0 ? (
            <ul>
              {state.entities.map((e) => (
                <li
                  key={e.id}
                  className="p-2 cursor-pointer hover:bg-gray-100 rounded"
                  onClick={() => setSelectedEntity(e)}
                >
                  {e.name}
                </li>
              ))}
            </ul>
          ) : (
            <p>Loading entities...</p>
          )}

          {selectedEntity && (
            <div className="mt-4 p-3 border rounded bg-gray-50">
              <h3 className="font-semibold">{selectedEntity.name}</h3>
              <p>ID: {selectedEntity.id}</p>
              <p>Patron Deity: {selectedEntity.patron?.name || "None"}</p>
              <button
                className="mt-2 px-2 py-1 border rounded hover:bg-gray-100"
                onClick={() => setSelectedEntity(null)}
              >
                Close
              </button>
            </div>
          )}
        </div>

        {/* Deities Panel */}
        <div className="md:w-1/2 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Deities</h2>
          {state.deities.length > 0 ? (
            <ul>
              {state.deities.map((d) => (
                <li
                  key={d.id}
                  className="p-2 cursor-pointer hover:bg-gray-100 rounded"
                  onClick={() => setSelectedDeity(d)}
                >
                  {d.name}
                </li>
              ))}
            </ul>
          ) : (
            <p>Loading deities...</p>
          )}

          {selectedDeity && (
            <div className="mt-4 p-3 border rounded bg-gray-50">
              <h3 className="font-semibold">{selectedDeity.name}</h3>
              <p>ID: {selectedDeity.id}</p>
              <p>Domain: {selectedDeity.domain}</p>
              <button
                className="mt-2 px-2 py-1 border rounded hover:bg-gray-100"
                onClick={() => setSelectedDeity(null)}
              >
                Close
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

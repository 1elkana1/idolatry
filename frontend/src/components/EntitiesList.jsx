import { useState } from "react";
import ActionModal from "./ActionModal"; // import the modal

export default function EntitiesList({ entities, fetchState }) {
  const [expanded, setExpanded] = useState(null);

  const toggleExpand = (name) =>
    setExpanded(expanded === name ? null : name);

  const [modal, setModal] = useState(null);

  const handleAttack = (entity) => {
    setModal({ type: "attack", entity });
  };

  const handleOffer = (entity) => {
    setModal({ type: "offer", entity });
  };

  return (
    <div className="mb-6">
      <h2 className="text-lg font-bold mb-2">Entities</h2>

      <ul className="space-y-2">
        {entities.map((e) => (
          <li key={e.name} className="border p-2 rounded">
            <div
              className="flex justify-between items-center cursor-pointer"
              onClick={() => toggleExpand(e.name)}
            >
              <span>
                <strong>{e.name}</strong>
                {e.patron_name && (
                  <span className="text-sm text-gray-500">
                    {" "} (Patron: {e.patron_name})
                  </span>
                )}
              </span>
              <span>
                💰 {e.wealth} | ⚔️ {e.army}
              </span>
            </div>

            {expanded === e.name && (
              <div className="mt-2 text-sm text-gray-600 space-y-2">
                {e.cults?.length > 0 ? (
                  <>
                    <div>Cults:</div>
                    <ul className="list-disc ml-6">
                      {e.cults.map((c, i) => (
                        <li key={i}>
                          {c.deity_name} (💰 {c.offerings})
                        </li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <div>No other cults</div>
                )}

                <div className="mt-2 flex gap-2">
                  <button
                    className="bg-red-500 text-white px-2 py-1 rounded"
                    onClick={() => setModal({ type: "attack", entity: e })}
                  >
                    Attack
                  </button>
                  <button
                    className="bg-yellow-500 text-white px-2 py-1 rounded"
                    onClick={() => setModal({ type: "offer", entity: e })}
                  >
                    Offer
                  </button>
                </div>

              </div>
            )}
          </li>
        ))}
      </ul>

      <ActionModal modal={modal} setModal={setModal} entities={entities} fetchState={fetchState} />
      
    </div>
  );
}

import { useState } from "react";

export default function ActionModal({ modal, setModal, entities, fetchState }) {
  const [targetId, setTargetId] = useState("");
  const [amount, setAmount] = useState("");

  if (!modal) return null;

  const handleAttack = async () => {
    if (!targetId) return;
    await fetch(`${import.meta.env.VITE_API_URL}/battle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        attacker_id: modal.entity.id,
        defender_id: parseInt(targetId),
      }),
    });
    setModal(null);
    fetchState();
  };

  const handleOffer = async () => {
    if (!targetId || !amount) return;
    await fetch(`${process.env.REACT_APP_API_URL}/offering`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        entity_id: modal.entity.id,
        deity_id: parseInt(targetId),
        amount: parseInt(amount),
      }),
    });
    setModal(null);
    fetchState();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h2 className="text-lg font-bold mb-4">
          {modal.type === "attack" ? "Attack Entity" : "Make Offering"}
        </h2>

        {modal.type === "attack" && (
          <div>
            <p>Attack with: {modal.entity.name}</p>
            <select
              className="border p-1 w-full mb-2"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value)}
            >
              <option value="">Select target</option>
              {entities
                .filter((e) => e.name !== modal.entity.name)
                .map((e) => (
                  <option key={e.name} value={e.id}>
                    {e.name}
                  </option>
                ))}
            </select>
            <button
              className="bg-red-500 text-white px-4 py-2 rounded"
              onClick={handleAttack}
            >
              Attack
            </button>
          </div>
        )}

        {modal.type === "offer" && (
          <div>
            <p>Offer from: {modal.entity.name}</p>
            <select
              className="border p-1 w-full mb-2"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value)}
            >
              <option value="">Select deity</option>
              {modal.entity.cults?.map((c) => (
                <option key={c.deity_id} value={c.deity_id}>
                  {c.deity_name}
                </option>
              ))}
            </select>
            <input
              type="number"
              className="border p-1 w-full mb-2"
              placeholder="Amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
            <button
              className="bg-yellow-500 text-white px-4 py-2 rounded"
              onClick={handleOffer}
            >
              Offer
            </button>
          </div>
        )}

        <button
          className="mt-4 text-sm underline text-gray-500"
          onClick={() => setModal(null)}
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
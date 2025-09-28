import { useState } from "react";

export default function DeitiesList({ deities }) {
  const [expanded, setExpanded] = useState(null);

  const toggleExpand = (name) =>
    setExpanded(expanded === name ? null : name);

  // Group by domain
  const grouped = deities.reduce((acc, d) => {
    if (!acc[d.domain]) acc[d.domain] = [];
    acc[d.domain].push(d);
    return acc;
  }, {});

  return (
    <div className="mb-6">
      <h2 className="text-lg font-bold mb-2">Deities</h2>
      {Object.entries(grouped).map(([domain, list]) => (
        <div key={domain} className="mb-4">
          <h3 className="text-md font-semibold mb-2">{domain}</h3>
          <ul className="space-y-2">
            {list.map((d) => (
              <li key={d.name} className="border p-2 rounded">
                <div
                  className="flex justify-between items-center cursor-pointer"
                  onClick={() => toggleExpand(d.name)}
                >
                  <span className="font-semibold">{d.name}</span>
                  <span>
                    💰{" "}
                    {d.cults?.reduce(
                      (acc, c) => acc + (c.offerings ?? 0),
                      0
                    ) || 0}
                  </span>
                </div>

                {expanded === d.name && (
                  <div className="mt-2 text-sm text-gray-600">
                    {d.cults?.length > 0 ? (
                      <>
                        <div>Cults:</div>
                        <ul className="list-disc ml-6">
                          {d.cults.map((c, i) => (
                            <li key={i}>{c.entity_name} - 💰 {c.offerings ?? 0}</li>
                          ))}
                        </ul>
                      </>
                    ) : (
                      <div>No cults</div>
                    )}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
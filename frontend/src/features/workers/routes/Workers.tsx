import { useEffect, useState } from "react";
import { workerService } from "../../../services/worker.service";
import type { Worker } from "../../../services/worker.service";

export default function Workers() {
  const [workers, setWorkers] = useState<Worker[]>([]);

  useEffect(() => {
    workerService.getWorkers().then(setWorkers);
  }, []);

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-4xl font-bold">Workers</h1>

        <button className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700">
          + Register Worker
        </button>
      </div>

      <div className="overflow-hidden rounded-2xl border border-zinc-800">
        <table className="w-full">
          <thead className="bg-zinc-800">
            <tr>
              <th className="px-6 py-5 text-left">Hostname</th>
              <th className="px-6 py-5 text-left">Status</th>
              <th className="px-6 py-5 text-left">Heartbeat</th>
              <th className="px-6 py-5 text-left">Created</th>
            </tr>
          </thead>

          <tbody>
            {workers.map((worker) => (
              <tr
                key={worker.id}
                className="border-t border-zinc-800 hover:bg-zinc-900"
              >
                <td className="px-6 py-5 font-medium">
                  {worker.hostname}
                </td>

                <td className="px-6 py-5">
                  <span
                    className={`rounded-full px-3 py-1 text-sm ${
                      worker.status === "idle"
                        ? "bg-green-500/20 text-green-400"
                        : worker.status === "busy"
                        ? "bg-blue-500/20 text-blue-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {worker.status}
                  </span>
                </td>

                <td className="px-6 py-5">
                  {new Date(worker.heartbeat).toLocaleString()}
                </td>

                <td className="px-6 py-5">
                  {new Date(worker.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
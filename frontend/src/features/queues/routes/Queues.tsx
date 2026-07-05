import { useEffect, useState } from "react";
import { queueService, type Queue } from "../../../services/queue.service";

export default function Queues() {
  const [queues, setQueues] = useState<Queue[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQueues();
  }, []);

  async function loadQueues() {
    try {
      const data = await queueService.getQueues();
      setQueues(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="p-6">Loading queues...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Queues</h1>

        <button className="rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700">
          + New Queue
        </button>
      </div>

      <div className="overflow-hidden rounded-xl border border-zinc-700">
        <table className="w-full">
          <thead className="bg-zinc-800 text-zinc-100">
            <tr>
              <th className="px-6 py-4 text-left">Name</th>
              <th className="px-6 py-4 text-left">Priority</th>
              <th className="px-6 py-4 text-left">Concurrency</th>
              <th className="px-6 py-4 text-left">Status</th>
              <th className="px-6 py-4 text-left">Created</th>
            </tr>
          </thead>

          <tbody>
            {queues.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="py-8 text-center text-zinc-400"
                >
                  No queues found.
                </td>
              </tr>
            ) : (
              queues.map((queue) => (
                <tr
                  key={queue.id}
                  className="border-t border-zinc-700 hover:bg-zinc-900 transition-colors"
                >
                  <td className="px-6 py-4">{queue.name}</td>

                  <td className="px-6 py-4">{queue.priority}</td>

                  <td className="px-6 py-4">
                    {queue.concurrency_limit}
                  </td>

                  <td className="px-6 py-4">
                    {queue.is_paused ? (
                      <span className="text-red-400">Paused</span>
                    ) : (
                      <span className="text-green-400">Running</span>
                    )}
                  </td>

                  <td className="px-6 py-4">
                    {new Date(queue.created_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
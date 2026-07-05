import { useEffect, useState } from "react";
import { dlqService } from "../../../services/dlq.service";
import type { DeadLetterJob } from "../../../services/dlq.service";

export default function DeadLetterQueue() {
  const [jobs, setJobs] = useState<DeadLetterJob[]>([]);

  useEffect(() => {
    dlqService.getDeadLetters().then(setJobs);
  }, []);

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-4xl font-bold">
          Dead Letter Queue
        </h1>
      </div>

      <div className="overflow-hidden rounded-2xl border border-zinc-800">
        <table className="w-full">
          <thead className="bg-zinc-800">
            <tr>
              <th className="px-6 py-5 text-left">
                Original Job
              </th>

              <th className="px-6 py-5 text-left">
                Reason
              </th>

              <th className="px-6 py-5 text-left">
                Payload
              </th>

              <th className="px-6 py-5 text-left">
                Failed At
              </th>
            </tr>
          </thead>

          <tbody>
            {jobs.map((job) => (
              <tr
                key={job.id}
                className="border-t border-zinc-800 hover:bg-zinc-900"
              >
                <td className="px-6 py-5 font-mono text-sm">
                  {job.original_job_id.slice(0, 8)}...
                </td>

                <td className="px-6 py-5">
                  <span className="rounded-full bg-red-500/20 px-3 py-1 text-sm text-red-400">
                    {job.reason}
                  </span>
                </td>

                <td className="max-w-sm truncate px-6 py-5">
                  {JSON.stringify(job.payload)}
                </td>

                <td className="px-6 py-5">
                  {new Date(job.failed_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {jobs.length === 0 && (
          <div className="py-12 text-center text-zinc-500">
            No jobs in Dead Letter Queue.
          </div>
        )}
      </div>
    </div>
  );
}
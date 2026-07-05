import { useEffect, useState } from "react";
import { jobService } from "../../../services/job.service";
import type { Job } from "../../../services/job.service";

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    jobService.getJobs().then(setJobs);
  }, []);

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-4xl font-bold">Jobs</h1>

        <button className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white hover:bg-blue-700">
          + New Job
        </button>
      </div>

      <div className="overflow-hidden rounded-2xl border border-zinc-800">
        <table className="w-full">
          <thead className="bg-zinc-800">
            <tr>
              <th className="px-6 py-5 text-left">Type</th>
              <th className="px-6 py-5 text-left">State</th>
              <th className="px-6 py-5 text-left">Priority</th>
              <th className="px-6 py-5 text-left">Attempts</th>
              <th className="px-6 py-5 text-left">Created</th>
            </tr>
          </thead>

          <tbody>
            {jobs.map((job) => (
              <tr
                key={job.id}
                className="border-t border-zinc-800 hover:bg-zinc-900"
              >
                <td className="px-6 py-5">{job.type}</td>

                <td className="px-6 py-5">
                  <span
                    className={`rounded-full px-3 py-1 text-sm ${
                      job.state === "completed"
                        ? "bg-green-500/20 text-green-400"
                        : job.state === "running"
                        ? "bg-blue-500/20 text-blue-400"
                        : job.state === "failed"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-yellow-500/20 text-yellow-400"
                    }`}
                  >
                    {job.state}
                  </span>
                </td>

                <td className="px-6 py-5">{job.priority}</td>

                <td className="px-6 py-5">{job.attempts}</td>

                <td className="px-6 py-5">
                  {new Date(job.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
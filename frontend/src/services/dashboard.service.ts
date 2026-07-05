import { api } from "../lib/api";
import type { DashboardStats } from "../types";

interface DashboardOverviewResponse {
  projects: number;
  queues: number;
  jobs: number;
  workers: number;
  queued_jobs: number;
  running_jobs: number;
  completed_jobs: number;
  failed_jobs: number;
  idle_workers: number;
  busy_workers: number;
  execution_logs: number;
}

export const dashboardService = {
  async getStats(
    timeframe: "24h" | "7d" | "30d" = "24h"
  ): Promise<DashboardStats> {
    const { data } = await api.get<DashboardOverviewResponse>(
      "/dashboard/overview",
      {
        params: { timeframe },
      }
    );

    return {
      total_projects: data.projects,
      total_queues: data.queues,
      active_workers: data.workers,
      jobs_completed: data.completed_jobs,
      jobs_failed: data.failed_jobs,
      jobs_running: data.running_jobs,
      jobs_queued: data.queued_jobs,
      execution_trend: [],
      status_distribution: [
        {
          name: "Completed",
          value: data.completed_jobs,
          color: "#22c55e",
        },
        {
          name: "Running",
          value: data.running_jobs,
          color: "#3b82f6",
        },
        {
          name: "Queued",
          value: data.queued_jobs,
          color: "#eab308",
        },
        {
          name: "Failed",
          value: data.failed_jobs,
          color: "#ef4444",
        },
      ],
    };
  },
};
import { api } from "../lib/api";

export interface Job {
  id: string;
  queue_id: string;
  retry_policy_id?: string;

  type: string;

  payload: Record<string, unknown>;

  state: string;

  priority: number;

  attempts: number;

  run_after: string;

  created_at: string;

  updated_at: string;
}

export const jobService = {
  async getJobs(): Promise<Job[]> {
    const { data } = await api.get<Job[]>("/jobs");
    return data;
  },
};
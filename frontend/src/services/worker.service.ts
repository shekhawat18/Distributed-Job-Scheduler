import { api } from "../lib/api";

export interface Worker {
  id: string;
  hostname: string;
  status: string;
  heartbeat: string;
  created_at: string;
}

export const workerService = {
  async getWorkers(): Promise<Worker[]> {
    const { data } = await api.get<Worker[]>("/workers");
    return data;
  },
};
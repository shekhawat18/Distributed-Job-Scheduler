import { api } from "../lib/api";

export interface DeadLetterJob {
  id: string;
  original_job_id: string;
  payload: Record<string, unknown>;
  reason: string;
  failed_at: string;
}

export const dlqService = {
  async getDeadLetters(): Promise<DeadLetterJob[]> {
    const { data } = await api.get<DeadLetterJob[]>("/dlq");
    return data;
  },
};
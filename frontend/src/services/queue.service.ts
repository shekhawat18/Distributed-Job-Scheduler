import { api } from "../lib/api";

export interface Queue {
  id: string;
  project_id: string;
  name: string;
  priority: number;
  concurrency_limit: number;
  is_paused: boolean;
  created_at: string;
}

export interface CreateQueueRequest {
  project_id: string;
  name: string;
  priority: number;
  concurrency_limit: number;
}

export interface UpdateQueueRequest {
  name?: string;
  priority?: number;
  concurrency_limit?: number;
  is_paused?: boolean;
}

export const queueService = {
  async getQueues(): Promise<Queue[]> {
    const { data } = await api.get<Queue[]>("/queues");
    return data;
  },

  async createQueue(queue: CreateQueueRequest): Promise<Queue> {
    const { data } = await api.post<Queue>("/queues", queue);
    return data;
  },

  async updateQueue(
    id: string,
    queue: UpdateQueueRequest
  ): Promise<Queue> {
    const { data } = await api.put<Queue>(`/queues/${id}`, queue);
    return data;
  },

  async deleteQueue(id: string): Promise<void> {
    await api.delete(`/queues/${id}`);
  },

  async pauseQueue(id: string): Promise<Queue> {
    const { data } = await api.post<Queue>(`/queues/${id}/pause`);
    return data;
  },

  async resumeQueue(id: string): Promise<Queue> {
    const { data } = await api.post<Queue>(`/queues/${id}/resume`);
    return data;
  },
};
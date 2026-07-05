export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'engineer' | 'viewer';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface StatusDistribution {
  name: string;
  value: number;
  color: string;
}

export interface ChartDataPoint {
  time: string;
  success: number;
  failed: number;
}

export interface DashboardStats {
  total_projects: number;
  total_queues: number;
  active_workers: number;
  jobs_completed: number;
  jobs_failed: number;
  jobs_running: number;
  jobs_queued: number;
  execution_trend: ChartDataPoint[];
  status_distribution: StatusDistribution[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface QueryParams {
  page?: number;
  size?: number;
  search?: string;
  status?: string;
}

export type JobStatus = 'queued' | 'running' | 'completed' | 'failed' | 'retrying';

export interface Job {
  id: string;
  queue_id: string;
  status: JobStatus;
  payload: Record<string, unknown>;
  priority: number;
  attempts: number;
  max_retries: number;
  error_message?: string | null;
  created_at: string;
  started_at?: string | null;
  completed_at?: string | null;
}

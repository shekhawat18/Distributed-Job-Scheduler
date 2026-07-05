import { api } from "../lib/api";

export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

export interface CreateProjectRequest {
  name: string;
  description: string;
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string;
}

export const projectService = {
  async getProjects(): Promise<Project[]> {
    const { data } = await api.get<Project[]>("/projects");
    return data;
  },

  async getProject(id: string): Promise<Project> {
    const { data } = await api.get<Project>(`/projects/${id}`);
    return data;
  },

  async createProject(
    project: CreateProjectRequest
  ): Promise<Project> {
    const { data } = await api.post<Project>("/projects", project);
    return data;
  },

  async updateProject(
    id: string,
    project: UpdateProjectRequest
  ): Promise<Project> {
    const { data } = await api.put<Project>(
      `/projects/${id}`,
      project
    );
    return data;
  },

  async deleteProject(id: string): Promise<void> {
    await api.delete(`/projects/${id}`);
  },
};
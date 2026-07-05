import { useEffect, useState } from "react";
import { projectService, type Project } from "../../../services/project.service";

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  const loadProjects = async () => {
    try {
      const data = await projectService.getProjects();
      setProjects(data);
    } catch (err) {
      console.error("Failed to load projects", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  if (loading) {
    return (
      <div className="p-6 text-lg">
        Loading projects...
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">
          Projects
        </h1>

        <button
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          + New Project
        </button>
      </div>

      <div className="overflow-hidden rounded-lg border">
        <table className="min-w-full">
          <thead className="bg-zinc-800 text-zinc-100">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold uppercase tracking-wide">Name</th>
              <th className="px-4 py-3 text-left">Description</th>
              <th className="px-4 py-3 text-left">Created</th>
            </tr>
          </thead>

          <tbody>
            {projects.length === 0 ? (
              <tr>
                <td
                  colSpan={3}
                  className="py-6 text-center text-gray-500"
                >
                  No projects found.
                </td>
              </tr>
            ) : (
              projects.map((project) => (
                <tr
  key={project.id}
  className="border-t border-zinc-700 hover:bg-zinc-900 transition-colors duration-200"
>
                  <td className="px-6 py-4 text-sm">
                    {project.name}
                  </td>

                  <td className="px-6 py-4 text-sm">
                    {project.description}
                  </td>

                 <td className="px-6 py-4 text-sm">
                    {new Date(project.created_at).toLocaleString()}
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
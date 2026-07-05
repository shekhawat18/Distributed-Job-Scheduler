import { lazy, Suspense, type ReactNode } from "react";
import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";

import { ErrorBoundary } from "./ErrorBoundary";
import { ProtectedRoute } from "../features/auth/routes/ProtectedRoute";
import { useAuth } from "../features/auth/context/AuthContext";
import { FullScreenLoader } from "../components/ui/FullScreenLoader";
import { DashboardLayout } from "../components/layouts/DashboardLayout";

// Lazy loaded pages
const Login = lazy(() => import("../features/auth/routes/Login"));
const Dashboard = lazy(() => import("../features/dashboard/routes/Dashboard"));
const Projects = lazy(() => import("../features/projects/routes/Projects"));
const Queues = lazy(() => import("../features/queues/routes/Queues"));
const Jobs = lazy(() => import("../features/jobs/routes/Jobs"));
const Workers = lazy(() => import("../features/workers/routes/Workers"));
const DeadLetterQueue = lazy(
  () => import("../features/dlq/routes/DeadLetterQueue")
);




// Prevent logged-in users from seeing login page
const PublicOnlyRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

const router = createBrowserRouter([
  {
    path: "/login",
    element: (
      <PublicOnlyRoute>
        <Suspense fallback={<FullScreenLoader />}>
          <Login />
        </Suspense>
      </PublicOnlyRoute>
    ),
  },
  {
    path: "/",
    element: <ProtectedRoute />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        element: <DashboardLayout />,
        children: [
          {
            index: true,
            element: <Navigate to="/dashboard" replace />,
          },
          {
            path: "dashboard",
            element: (
              <Suspense fallback={<FullScreenLoader />}>
                <Dashboard />
              </Suspense>
            ),
          },
          {
            path: "projects",
            element: (
              <Suspense fallback={<FullScreenLoader />}>
                <Projects />
              </Suspense>
            ),
          },
          {
  path: "queues",
  element: (
    <Suspense fallback={<FullScreenLoader />}>
      <Queues />
    </Suspense>
  ),
},
          {
  path: "jobs",
  element: (
    <Suspense fallback={<FullScreenLoader />}>
      <Jobs />
    </Suspense>
  ),
},
          {
  path: "workers",
  element: (
    <Suspense fallback={<FullScreenLoader />}>
      <Workers />
    </Suspense>
  ),
},
          {
  path: "dlq",
  element: (
    <Suspense fallback={<FullScreenLoader />}>
      <DeadLetterQueue />
    </Suspense>
  ),
},
        ],
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" replace />,
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
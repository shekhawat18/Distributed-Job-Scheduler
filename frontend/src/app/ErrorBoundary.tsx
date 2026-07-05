import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";
import { AlertCircle } from "lucide-react";

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: undefined,
  };

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("Uncaught error:", error, errorInfo);

    // Future: Send error to Sentry or another monitoring service
    // captureException(error);
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-gray-950 p-4 text-white">
          <div className="max-w-md rounded-xl border border-gray-800 bg-gray-900 p-8 text-center shadow-2xl">
            <AlertCircle className="mx-auto mb-4 h-12 w-12 text-red-500" />

            <h1 className="mb-2 text-2xl font-bold">
              Something went wrong
            </h1>

            <p className="mb-6 text-sm text-gray-400">
              {this.state.error?.message ??
                "An unexpected error occurred."}
            </p>

            <button
              onClick={() => window.location.reload()}
              className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return <>{this.props.children}</>;
  }
}
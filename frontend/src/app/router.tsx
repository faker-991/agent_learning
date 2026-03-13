import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";

function PlaceholderPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">
          Business Research Workbench
        </p>
        <h1 className="mt-4 max-w-3xl text-5xl font-semibold tracking-tight">
          React workspace scaffold is ready for the project-based redesign.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
          The next implementation chunks will replace this placeholder with project,
          task, evidence, and conclusion-card workflows.
        </p>
        <div className="mt-10 flex flex-wrap gap-4">
          <Link className="rounded-full bg-cyan-400 px-5 py-3 text-sm font-medium text-slate-950" to="/projects">
            Open projects route
          </Link>
          <span className="rounded-full border border-slate-700 px-5 py-3 text-sm text-slate-300">
            Current route scaffold only
          </span>
        </div>
      </div>
    </main>
  );
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/projects" replace />} />
        <Route path="/projects" element={<PlaceholderPage />} />
      </Routes>
    </BrowserRouter>
  );
}

import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter, Link, Navigate, Route, Routes } from "react-router-dom";
function PlaceholderPage() {
    return (_jsx("main", { className: "min-h-screen bg-slate-950 text-slate-50", children: _jsxs("div", { className: "mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-16", children: [_jsx("p", { className: "text-sm uppercase tracking-[0.3em] text-cyan-300", children: "Business Research Workbench" }), _jsx("h1", { className: "mt-4 max-w-3xl text-5xl font-semibold tracking-tight", children: "React workspace scaffold is ready for the project-based redesign." }), _jsx("p", { className: "mt-6 max-w-2xl text-lg leading-8 text-slate-300", children: "The next implementation chunks will replace this placeholder with project, task, evidence, and conclusion-card workflows." }), _jsxs("div", { className: "mt-10 flex flex-wrap gap-4", children: [_jsx(Link, { className: "rounded-full bg-cyan-400 px-5 py-3 text-sm font-medium text-slate-950", to: "/projects", children: "Open projects route" }), _jsx("span", { className: "rounded-full border border-slate-700 px-5 py-3 text-sm text-slate-300", children: "Current route scaffold only" })] })] }) }));
}
export function AppRouter() {
    return (_jsx(BrowserRouter, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(Navigate, { to: "/projects", replace: true }) }), _jsx(Route, { path: "/projects", element: _jsx(PlaceholderPage, {}) })] }) }));
}

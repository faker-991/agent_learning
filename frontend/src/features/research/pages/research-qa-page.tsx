import { useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { MemoryContextPanel } from "../components/memory-context-panel";
import { PaperResultPanel } from "../components/paper-result-panel";
import { ResearchCardPanel } from "../components/research-card-panel";
import {
  generateSessionPlan,
  getResearchCard,
  getSession,
  listSessionEvents,
  runSession,
} from "../api";

export function ResearchQaPage() {
  const { sessionId = "" } = useParams();
  const queryClient = useQueryClient();

  const sessionQuery = useQuery({
    queryKey: ["session", sessionId],
    queryFn: () => getSession(sessionId),
    enabled: Boolean(sessionId),
  });

  const eventsQuery = useQuery({
    queryKey: ["session", sessionId, "events"],
    queryFn: () => listSessionEvents(sessionId),
    enabled: Boolean(sessionId),
    refetchInterval: 3000,
  });

  const cardQuery = useQuery({
    queryKey: ["session", sessionId, "research-card"],
    queryFn: () => getResearchCard(sessionId),
    enabled: sessionQuery.data?.status === "completed",
  });

  const refresh = () => {
    queryClient.invalidateQueries({ queryKey: ["session", sessionId] });
    queryClient.invalidateQueries({ queryKey: ["session", sessionId, "events"] });
    queryClient.invalidateQueries({ queryKey: ["session", sessionId, "research-card"] });
  };

  const planMutation = useMutation({
    mutationFn: () => generateSessionPlan(sessionId),
    onSuccess: refresh,
  });

  const runMutation = useMutation({
    mutationFn: () => runSession(sessionId),
    onSuccess: refresh,
  });

  const memoryNotes = useMemo(
    () => (eventsQuery.data?.events ?? []).filter((event) => event.stage === "memory").map((event) => event.message),
    [eventsQuery.data],
  );

  const session = sessionQuery.data;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-6">
          <Link
            to={session ? `/topics/${session.workspace_id}` : "/topics"}
            className="text-sm text-cyan-300 hover:text-cyan-200"
          >
            ← Back to topic
          </Link>
        </div>

        <div className="grid gap-6 xl:grid-cols-[0.78fr_1fr_0.92fr]">
          <MemoryContextPanel notes={memoryNotes} />

          <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-6">
            <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Research</p>
            <h1 className="mt-4 text-2xl font-semibold">
              {session?.question ?? "Loading research round..."}
            </h1>
            <p className="mt-4 text-sm leading-7 text-slate-300">
              Intent: {session?.intent_type?.replace(/_/g, " ") ?? "unknown"}
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <button
                type="button"
                disabled={planMutation.isPending}
                onClick={() => planMutation.mutate()}
                className="rounded-2xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500"
              >
                {planMutation.isPending ? "Planning..." : "Generate plan"}
              </button>
              <button
                type="button"
                disabled={runMutation.isPending}
                onClick={() => runMutation.mutate()}
                className="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-white disabled:cursor-not-allowed disabled:bg-slate-800 disabled:text-slate-500"
              >
                {runMutation.isPending ? "Running..." : "Run session"}
              </button>
            </div>

            <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="text-sm font-medium text-slate-200">Plan snapshot</p>
              <pre className="mt-3 overflow-auto whitespace-pre-wrap text-xs leading-6 text-slate-400">
                {session?.plan_snapshot
                  ? JSON.stringify(session.plan_snapshot, null, 2)
                  : "No plan generated yet."}
              </pre>
            </div>

            <div className="mt-6 space-y-3">
              {(eventsQuery.data?.events ?? []).map((event) => (
                <div key={event.id} className="rounded-3xl border border-slate-800 bg-slate-950/60 p-4">
                  <div className="flex items-center justify-between gap-4">
                    <strong className="text-sm uppercase tracking-[0.18em] text-cyan-200">
                      {event.stage}
                    </strong>
                    <span className="text-xs text-slate-500">{event.type}</span>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-slate-300">{event.message}</p>
                </div>
              ))}
            </div>
          </section>

          <div className="space-y-6">
            <PaperResultPanel paperIds={session?.selected_paper_ids ?? []} />
            <ResearchCardPanel card={cardQuery.data} />
          </div>
        </div>
      </div>
    </main>
  );
}


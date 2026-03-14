import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { getTopic } from "../api";
import { createSession, listTopicSessions } from "../../research/api";

const intentOptions = [
  { value: "find_representative_papers", label: "Find representative papers" },
  { value: "compare_methods", label: "Compare several methods" },
  { value: "research_gap", label: "Look for research gaps" },
];

export function TopicHomePage() {
  const { topicId = "" } = useParams();
  const queryClient = useQueryClient();
  const [question, setQuestion] = useState("");
  const [intentType, setIntentType] = useState("find_representative_papers");
  const [timeWindowYears, setTimeWindowYears] = useState(2);

  const topicQuery = useQuery({
    queryKey: ["topic", topicId],
    queryFn: () => getTopic(topicId),
    enabled: Boolean(topicId),
  });

  const sessionsQuery = useQuery({
    queryKey: ["topic", topicId, "sessions"],
    queryFn: () => listTopicSessions(topicId),
    enabled: Boolean(topicId),
  });

  const createSessionMutation = useMutation({
    mutationFn: () =>
      createSession(topicId, {
        question,
        intent_type: intentType,
        time_window_years: timeWindowYears,
      }),
    onSuccess: () => {
      setQuestion("");
      queryClient.invalidateQueries({ queryKey: ["topic", topicId, "sessions"] });
    },
  });

  const statusSummary = useMemo(() => {
    const items = sessionsQuery.data ?? [];
    return {
      total: items.length,
      active: items.filter((item) => item.status !== "completed").length,
      completed: items.filter((item) => item.status === "completed").length,
    };
  }, [sessionsQuery.data]);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8 flex items-center justify-between gap-4">
          <div>
            <Link to="/topics" className="text-sm text-cyan-300 hover:text-cyan-200">
              ← Back to topics
            </Link>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight">
              {topicQuery.data?.title ?? "Loading topic..."}
            </h1>
            <p className="mt-3 max-w-3xl text-base leading-7 text-slate-400">
              {topicQuery.data?.description || "Use this topic to retrieve recent papers and build topic memory."}
            </p>
          </div>
          <div className="grid min-w-56 gap-3 rounded-3xl border border-slate-800 bg-slate-900/70 p-5 text-sm text-slate-300">
            <div className="flex justify-between">
              <span>Total sessions</span>
              <strong>{statusSummary.total}</strong>
            </div>
            <div className="flex justify-between">
              <span>Active</span>
              <strong>{statusSummary.active}</strong>
            </div>
            <div className="flex justify-between">
              <span>Completed</span>
              <strong>{statusSummary.completed}</strong>
            </div>
          </div>
        </div>

        <div className="grid gap-8 xl:grid-cols-[0.92fr_1.08fr]">
          <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8">
            <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">New research round</p>
            <h2 className="mt-4 text-2xl font-semibold">Ask a research question</h2>
            <form
              className="mt-6 space-y-4"
              onSubmit={(event) => {
                event.preventDefault();
                if (!question.trim()) return;
                createSessionMutation.mutate();
              }}
            >
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Research question</span>
                <textarea
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  className="min-h-40 w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none focus:border-cyan-400"
                  placeholder="What are the recent representative papers for agent search?"
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Intent</span>
                <select
                  value={intentType}
                  onChange={(event) => setIntentType(event.target.value)}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none focus:border-cyan-400"
                >
                  {intentOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Time window</span>
                <input
                  type="number"
                  min={1}
                  value={timeWindowYears}
                  onChange={(event) => setTimeWindowYears(Number(event.target.value))}
                  className="w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none focus:border-cyan-400"
                />
              </label>
              <button
                type="submit"
                disabled={createSessionMutation.isPending}
                className="w-full rounded-2xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-cyan-900 disabled:text-cyan-100"
              >
                {createSessionMutation.isPending ? "Creating..." : "Create research round"}
              </button>
            </form>
          </section>

          <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8">
            <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Recent sessions</p>
            <h2 className="mt-4 text-2xl font-semibold">Topic history</h2>

            <div className="mt-6 grid gap-4">
              {sessionsQuery.isLoading ? (
                <p className="rounded-3xl border border-slate-800 bg-slate-950/60 px-5 py-8 text-slate-400">
                  Loading sessions...
                </p>
              ) : sessionsQuery.data?.length ? (
                sessionsQuery.data.map((session) => (
                  <Link
                    key={session.id}
                    to={`/sessions/${session.id}`}
                    className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5 transition hover:border-cyan-400/50"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="text-lg font-semibold">{session.question}</h3>
                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {session.intent_type.replace(/_/g, " ")}
                        </p>
                      </div>
                      <span className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.2em] text-slate-300">
                        {session.status}
                      </span>
                    </div>
                  </Link>
                ))
              ) : (
                <p className="rounded-3xl border border-dashed border-slate-700 bg-slate-950/60 px-5 py-8 text-slate-400">
                  No sessions yet. Create one to start the research flow.
                </p>
              )}
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}


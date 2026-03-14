import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { createTopic, listTopics } from "../api";

export function TopicListPage() {
  const queryClient = useQueryClient();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [researchDomain, setResearchDomain] = useState("ai");

  const topicsQuery = useQuery({
    queryKey: ["topics"],
    queryFn: listTopics,
  });

  const createTopicMutation = useMutation({
    mutationFn: createTopic,
    onSuccess: () => {
      setTitle("");
      setDescription("");
      queryClient.invalidateQueries({ queryKey: ["topics"] });
    },
  });

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr]">
          <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8 shadow-2xl shadow-cyan-950/20">
            <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Topics</p>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight">
              Literature research workspace
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
              Organize research topics, retrieve representative papers, and build durable
              topic memory around papers, notes, and hypotheses.
            </p>

            <div className="mt-8 grid gap-4">
              {topicsQuery.isLoading ? (
                <p className="rounded-3xl border border-slate-800 bg-slate-950/70 px-5 py-8 text-slate-400">
                  Loading topics...
                </p>
              ) : topicsQuery.data?.length ? (
                topicsQuery.data.map((topic) => (
                  <Link
                    key={topic.id}
                    to={`/topics/${topic.id}`}
                    className="group rounded-3xl border border-slate-800 bg-slate-950/70 p-5 transition hover:border-cyan-400/50 hover:bg-slate-900"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h2 className="text-xl font-semibold text-slate-100 group-hover:text-cyan-200">
                          {topic.title}
                        </h2>
                        <p className="mt-2 text-sm leading-6 text-slate-400">
                          {topic.description || "No description yet."}
                        </p>
                      </div>
                      <span className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.2em] text-slate-400">
                        {topic.research_domain}
                      </span>
                    </div>
                  </Link>
                ))
              ) : (
                <p className="rounded-3xl border border-dashed border-slate-700 bg-slate-950/70 px-5 py-8 text-slate-400">
                  No topics yet. Create the first one on the right.
                </p>
              )}
            </div>
          </section>

          <aside className="rounded-[2rem] border border-slate-800 bg-[linear-gradient(160deg,rgba(8,47,73,0.92),rgba(15,23,42,0.92))] p-8 shadow-2xl shadow-cyan-950/20">
            <p className="text-sm uppercase tracking-[0.28em] text-cyan-200">New topic</p>
            <h2 className="mt-4 text-2xl font-semibold">Start a research track</h2>
            <form
              className="mt-6 space-y-4"
              onSubmit={(event) => {
                event.preventDefault();
                if (!title.trim()) return;
                createTopicMutation.mutate({
                  title,
                  description: description || undefined,
                  research_domain: researchDomain,
                });
              }}
            >
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Topic title</span>
                <input
                  className="w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none ring-0 placeholder:text-slate-500 focus:border-cyan-400"
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  placeholder="Agent Search"
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Description</span>
                <textarea
                  className="min-h-32 w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-cyan-400"
                  value={description}
                  onChange={(event) => setDescription(event.target.value)}
                  placeholder="What problem or direction are you tracking?"
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-sm text-slate-300">Domain</span>
                <input
                  className="w-full rounded-2xl border border-slate-700 bg-slate-950/60 px-4 py-3 outline-none placeholder:text-slate-500 focus:border-cyan-400"
                  value={researchDomain}
                  onChange={(event) => setResearchDomain(event.target.value)}
                />
              </label>

              <button
                type="submit"
                disabled={createTopicMutation.isPending}
                className="w-full rounded-2xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:bg-cyan-900 disabled:text-cyan-100"
              >
                {createTopicMutation.isPending ? "Creating..." : "Create topic"}
              </button>
            </form>
          </aside>
        </div>
      </div>
    </main>
  );
}


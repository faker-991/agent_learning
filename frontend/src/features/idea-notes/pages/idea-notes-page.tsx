import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { listTopicIdeas } from "../api";

export function IdeaNotesPage() {
  const { topicId = "" } = useParams();
  const ideasQuery = useQuery({
    queryKey: ["topic", topicId, "ideas"],
    queryFn: () => listTopicIdeas(topicId),
    enabled: Boolean(topicId),
  });

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-50">
      <div className="mx-auto max-w-4xl rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8">
        <Link to={topicId ? `/topics/${topicId}` : "/topics"} className="text-sm text-cyan-300 hover:text-cyan-200">
          ← Back to topic
        </Link>
        <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Idea notes</p>
        <h1 className="mt-4 text-3xl font-semibold">Ideas and hypotheses</h1>
        <div className="mt-6 space-y-4">
          {ideasQuery.data?.length ? (
            ideasQuery.data.map((idea) => (
              <section key={idea.id} className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
                <h2 className="text-xl font-semibold">{idea.title}</h2>
                <p className="mt-3 text-sm leading-7 text-slate-300">{idea.content}</p>
              </section>
            ))
          ) : (
            <p className="text-slate-400">No idea notes yet.</p>
          )}
        </div>
      </div>
    </main>
  );
}

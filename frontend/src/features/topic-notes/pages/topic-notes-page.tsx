import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { listTopicNotes } from "../api";

export function TopicNotesPage() {
  const { topicId = "" } = useParams();
  const notesQuery = useQuery({
    queryKey: ["topic", topicId, "notes"],
    queryFn: () => listTopicNotes(topicId),
    enabled: Boolean(topicId),
  });

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-50">
      <div className="mx-auto max-w-4xl rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8">
        <Link to={topicId ? `/topics/${topicId}` : "/topics"} className="text-sm text-cyan-300 hover:text-cyan-200">
          ← Back to topic
        </Link>
        <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Topic notes</p>
        <h1 className="mt-4 text-3xl font-semibold">Topic notes</h1>
        <div className="mt-6 space-y-4">
          {notesQuery.data?.length ? (
            notesQuery.data.map((note) => (
              <section key={note.id} className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
                <h2 className="text-xl font-semibold">{note.title}</h2>
                <p className="mt-3 text-sm leading-7 text-slate-300">{note.summary}</p>
              </section>
            ))
          ) : (
            <p className="text-slate-400">No topic notes yet.</p>
          )}
        </div>
      </div>
    </main>
  );
}

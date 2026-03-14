import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import { listTopicPapers } from "../api";

export function PaperCardPage() {
  const { paperId = "" } = useParams();
  const topicId = new URLSearchParams(window.location.search).get("topicId") ?? "";
  const papersQuery = useQuery({
    queryKey: ["topic", topicId, "papers"],
    queryFn: () => listTopicPapers(topicId),
    enabled: Boolean(topicId),
  });
  const paper = papersQuery.data?.find((item) => item.id === paperId);

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-50">
      <div className="mx-auto max-w-4xl rounded-[2rem] border border-slate-800 bg-slate-900/70 p-8">
        <Link to={topicId ? `/topics/${topicId}` : "/topics"} className="text-sm text-cyan-300 hover:text-cyan-200">
          ← Back to topic
        </Link>
        <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Paper card</p>
        <h1 className="mt-4 text-3xl font-semibold">{paper?.title ?? "Paper details"}</h1>
        {!paper ? (
          <p className="mt-4 text-slate-400">No paper details available.</p>
        ) : (
          <div className="mt-6 grid gap-4">
            <section className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Abstract</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">{paper.abstract}</p>
            </section>
            <section className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Method</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">{paper.method}</p>
            </section>
            <section className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Meta</p>
              <p className="mt-3 text-sm leading-7 text-slate-300">
                {paper.venue} · {paper.year}
              </p>
              <a className="mt-3 inline-block text-sm text-cyan-300 hover:text-cyan-200" href={paper.url} target="_blank" rel="noreferrer">
                Open PDF
              </a>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}

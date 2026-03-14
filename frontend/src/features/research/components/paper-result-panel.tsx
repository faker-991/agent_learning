type PaperResultPanelProps = {
  paperIds: string[];
};

export function PaperResultPanel({ paperIds }: PaperResultPanelProps) {
  return (
    <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-6">
      <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Representative papers</p>
      <h2 className="mt-4 text-2xl font-semibold">Selected papers</h2>
      <div className="mt-6 space-y-3">
        {paperIds.length ? (
          paperIds.map((paperId) => (
            <div
              key={paperId}
              className="rounded-3xl border border-slate-800 bg-slate-950/60 p-4 text-sm leading-6 text-slate-300"
            >
              {paperId}
            </div>
          ))
        ) : (
          <p className="rounded-3xl border border-dashed border-slate-700 bg-slate-950/60 px-4 py-8 text-slate-400">
            No representative papers have been selected yet.
          </p>
        )}
      </div>
    </section>
  );
}


type MemoryContextPanelProps = {
  notes: string[];
};

export function MemoryContextPanel({ notes }: MemoryContextPanelProps) {
  return (
    <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-6">
      <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Memory</p>
      <h2 className="mt-4 text-2xl font-semibold">Recalled context</h2>
      <div className="mt-6 space-y-3">
        {notes.length ? (
          notes.map((note) => (
            <div key={note} className="rounded-3xl border border-slate-800 bg-slate-950/60 p-4 text-sm leading-6 text-slate-300">
              {note}
            </div>
          ))
        ) : (
          <p className="rounded-3xl border border-dashed border-slate-700 bg-slate-950/60 px-4 py-8 text-slate-400">
            No recalled memory yet.
          </p>
        )}
      </div>
    </section>
  );
}


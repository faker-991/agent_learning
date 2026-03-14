import type { ResearchCard } from "../../../entities/research-card";

type ResearchCardPanelProps = {
  card?: ResearchCard;
};

export function ResearchCardPanel({ card }: ResearchCardPanelProps) {
  return (
    <section className="rounded-[2rem] border border-slate-800 bg-slate-900/70 p-6">
      <p className="text-sm uppercase tracking-[0.28em] text-cyan-300">Research card</p>
      <h2 className="mt-4 text-2xl font-semibold">Guidance output</h2>
      {!card ? (
        <p className="mt-6 rounded-3xl border border-dashed border-slate-700 bg-slate-950/60 px-5 py-8 text-slate-400">
          No research card yet.
        </p>
      ) : (
        <div className="mt-6 grid gap-4">
          <Section title="Problem definition" items={[card.problem_definition]} />
          <Section title="Method tracks" items={card.main_method_tracks} />
          <Section title="Method differences" items={card.method_differences} />
          <Section title="Research gaps" items={card.research_gaps} />
          <Section title="Improvement directions" items={card.improvement_directions} />
          <Section title="Reading order" items={card.reading_order} />
        </div>
      )}
    </section>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-950/60 p-5">
      <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{title}</p>
      <ul className="mt-4 space-y-3 text-sm leading-7 text-slate-200">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}


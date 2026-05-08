import type { Highlight } from "@/types/api";

type HighlightStripProps = {
  highlights: Highlight[];
};

export function HighlightStrip({ highlights }: HighlightStripProps) {
  if (!highlights.length) {
    return null;
  }

  return (
    <section className="highlight-strip" aria-label="Challenge highlights">
      {highlights.map((highlight) => (
        <article key={`${highlight.label}-${highlight.value}`}>
          <span>{highlight.label}</span>
          <strong>{highlight.value}</strong>
          <p>{highlight.detail}</p>
        </article>
      ))}
    </section>
  );
}

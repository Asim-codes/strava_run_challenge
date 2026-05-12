import { earnedBadges, stealableCrowns } from "@/lib/badges";

export default function BadgesPage() {
  return (
    <main className="badges-page">
      <section className="hero-card">
        <div>
          <p className="eyebrow">Reference</p>
          <h1>Badge rules</h1>
          <p>How badges are earned on the scoreboard.</p>
        </div>
      </section>

      <article className="section-card badges-rules">
        <section className="badges-section">
          <h2>Stealable Crowns</h2>
          <div className="badges-grid">
            {stealableCrowns.map((badge) => (
              <article className="badge-card" key={badge.name}>
                <h3 className="badge-card__title">
                  <span className="soft-badge">{badge.name}</span>
                </h3>
                <p>{badge.description}</p>
              </article>
            ))}
          </div>
        </section>

        {earnedBadges.map((category) => (
          <section className="badges-section" key={category.title}>
            <h2>{category.title}</h2>
            <div className="badges-grid">
              {category.badges.map((badge) => (
                <article className="badge-card" key={badge.name}>
                  <h3 className="badge-card__title">
                    <span className="soft-badge">{badge.name}</span>
                  </h3>
                  <p>{badge.description}</p>
                </article>
              ))}
            </div>
          </section>
        ))}
      </article>
    </main>
  );
}

import { ProgressBar } from "@/components/ProgressBar";
import type { IndividualStanding } from "@/types/api";

type IndividualLeaderboardProps = {
  individuals: IndividualStanding[];
};

export function IndividualLeaderboard({ individuals }: IndividualLeaderboardProps) {
  return (
    <section className="section-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Solo chase</p>
          <h2>Top runners</h2>
        </div>
        <span>Top {Math.min(individuals.length, 12)}</span>
      </div>

      <div className="ranking-list compact">
        {individuals.slice(0, 12).map((runner) => (
          <article className="ranking-card" key={`${runner.runner}-${runner.team}`}>
            <div className="rank-badge">{runner.medal ?? runner.rank}</div>
            <div className="ranking-main">
              <div className="ranking-title-row">
                <div>
                  <h3>{runner.runner}</h3>
                </div>
                <strong>{runner.distance.toFixed(1)} km</strong>
              </div>
              <ProgressBar value={runner.progress} />
              <div className="badge-row">
                <span>{runner.runs} runs</span>
                {runner.streak_weeks > 0 && (
                  <span>{runner.streak_weeks} active weeks</span>
                )}
                {runner.badges.map((badge) => (
                  <span className="soft-badge" key={badge}>
                    {badge}
                  </span>
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

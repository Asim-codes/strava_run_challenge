import { ProgressBar } from "@/components/ProgressBar";
import type { TeamContribution } from "@/types/api";

type ContributionBoardProps = {
  contributions: Record<string, TeamContribution[]>;
};

const SPLIT_COLORS = ["#f97316", "#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#14b8a6"];

export function ContributionBoard({ contributions }: ContributionBoardProps) {
  const teams = Object.entries(contributions).slice(0, 4);

  if (!teams.length) {
    return null;
  }

  return (
    <section className="section-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Teamwork</p>
          <h2>Contribution splits</h2>
        </div>
        <span>Top teams</span>
      </div>

      <div className="contribution-grid">
        {teams.map(([team, runners]) => {
          const totalDistance = runners.reduce(
            (total, runner) => total + runner.distance,
            0,
          );

          return (
            <article className="contribution-card" key={team}>
              <div className="contribution-header">
                <div>
                  <h3>{team}</h3>
                  <p>{runners.length} runners sharing the load</p>
                </div>
                <strong>{totalDistance.toFixed(1)} km</strong>
              </div>

              <div className="stacked-split" aria-label={`${team} contribution split`}>
                {runners.map((runner, index) => {
                  const share = totalDistance
                    ? (runner.distance / totalDistance) * 100
                    : 0;

                  return (
                    <span
                      key={`${team}-${runner.runner}-share`}
                      style={{
                        width: `${share}%`,
                        background: SPLIT_COLORS[index % SPLIT_COLORS.length],
                      }}
                      title={`${runner.runner}: ${share.toFixed(0)}%`}
                    />
                  );
                })}
              </div>

              <div className="contribution-list">
                {runners.map((runner, index) => {
                  const share = totalDistance
                    ? (runner.distance / totalDistance) * 100
                    : 0;
                  const color = SPLIT_COLORS[index % SPLIT_COLORS.length];

                  return (
                    <div className="contribution-member" key={`${team}-${runner.runner}`}>
                      <div className="contribution-row">
                        <span>
                          <i style={{ background: color }} />
                          {index + 1}. {runner.runner}
                        </span>
                        <strong>{runner.distance.toFixed(1)} km</strong>
                      </div>
                      <ProgressBar value={runner.progress} color={color} />
                      <div className="contribution-footnote">
                        <span>{share.toFixed(0)}% of team distance</span>
                        <span>{runner.runs} runs</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

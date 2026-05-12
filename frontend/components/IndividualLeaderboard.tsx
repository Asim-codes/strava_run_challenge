"use client";

import { useState } from "react";
import { ProgressBar } from "@/components/ProgressBar";
import type { IndividualStanding } from "@/types/api";

const DEFAULT_VISIBLE = 10;

type IndividualLeaderboardProps = {
  individuals: IndividualStanding[];
};

export function IndividualLeaderboard({ individuals }: IndividualLeaderboardProps) {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? individuals : individuals.slice(0, DEFAULT_VISIBLE);
  const hasMore = individuals.length > DEFAULT_VISIBLE;

  return (
    <section className="section-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Solo chase</p>
          <h2>Top runners</h2>
        </div>
        <span>{individuals.length} runners</span>
      </div>

      <div className="ranking-list compact">
        {visible.map((runner) => (
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
              </div>
              {runner.badges.length > 0 && (
                <details className="badges-details">
                  <summary>Badges ({runner.badges.length})</summary>
                  <div className="badge-row">
                    {runner.badges.map((badge) => (
                      <span className="soft-badge" key={badge}>
                        {badge}
                      </span>
                    ))}
                  </div>
                </details>
              )}
            </div>
          </article>
        ))}
      </div>

      {hasMore && (
        <button
          className="view-more-btn"
          onClick={() => setExpanded((prev) => !prev)}
        >
          {expanded
            ? "Show less"
            : `View ${individuals.length - DEFAULT_VISIBLE} more`}
        </button>
      )}
    </section>
  );
}

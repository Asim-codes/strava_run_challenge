import { ContributionBoard } from "@/components/ContributionBoard";
import { EmptyState } from "@/components/EmptyState";
import { IndividualLeaderboard } from "@/components/IndividualLeaderboard";
import { MetricCard } from "@/components/MetricCard";
import { TeamLeaderboard } from "@/components/TeamLeaderboard";
import { getCurrentChallenge } from "@/lib/api";

export default async function Home() {
  const challenge = await getCurrentChallenge().catch(() => null);

  if (!challenge) {
    return (
      <EmptyState
        title="The scoreboard needs the API"
        message="Start the FastAPI backend and check the Google Sheets environment variables."
      />
    );
  }

  if (challenge.summary.total_runs === 0) {
    return (
      <EmptyState
        title="No runs logged yet"
        message="Once the Google Sheet has current activities, the scoreboard will light up here."
      />
    );
  }

  const closestChase = challenge.highlights.find(
    (highlight) => highlight.label === "Closest chase",
  );

  return (
    <main>
      <section className="hero-card">
        <div>
          <p className="eyebrow">Current challenge</p>
          <h1>The monthly run-down</h1>
          <p>Run and vibes.</p>
        </div>
        <div className="days-pill">
          <strong>{challenge.summary.days_left}</strong>
          <span>days left</span>
        </div>
      </section>

      <details className="stats-panel" open>
        <summary>
          <span>Challenge snapshot</span>
          <strong>Tap to collapse</strong>
        </summary>
        <section className="metric-grid" aria-label="Challenge statistics">
          <MetricCard
            label="Total distance"
            value={`${challenge.summary.total_distance.toFixed(1)} km`}
            detail="Logged by everyone"
          />
          <MetricCard
            label="Total runs"
            value={challenge.summary.total_runs.toLocaleString()}
            detail="Efforts on the board"
          />
          <MetricCard
            label="Average run"
            value={`${challenge.summary.average_distance.toFixed(1)} km`}
            detail="Nice and steady"
          />
          <MetricCard
            label="Closest chase"
            value={closestChase?.value ?? "Not yet"}
            detail={closestChase?.detail ?? "Waiting for two teams to log runs."}
          />
        </section>
      </details>

      <TeamLeaderboard teams={challenge.teams} />
      <IndividualLeaderboard individuals={challenge.individuals} />
      <ContributionBoard contributions={challenge.contributions} />
    </main>
  );
}

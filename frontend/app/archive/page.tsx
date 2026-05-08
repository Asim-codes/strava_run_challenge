import { EmptyState } from "@/components/EmptyState";
import { HighlightStrip } from "@/components/HighlightStrip";
import { IndividualLeaderboard } from "@/components/IndividualLeaderboard";
import { MetricCard } from "@/components/MetricCard";
import { TeamLeaderboard } from "@/components/TeamLeaderboard";
import { getArchivePeriod, getArchivePeriods } from "@/lib/api";

type ArchivePageProps = {
  searchParams: Promise<{
    period?: string;
  }>;
};

export default async function ArchivePage({ searchParams }: ArchivePageProps) {
  const periods = await getArchivePeriods().catch(() => null);

  if (!periods) {
    return (
      <EmptyState
        title="Archive is waiting on the API"
        message="Start the backend and confirm archived rows include Archive and Period values."
      />
    );
  }

  if (!periods.length) {
    return (
      <EmptyState
        title="No archived periods yet"
        message="Archived rows with a Period value will appear here."
      />
    );
  }

  const params = await searchParams;
  const selectedPeriod = params.period ?? periods[0].period;
  const archive = await getArchivePeriod(selectedPeriod).catch(() => null);

  if (!archive) {
    return (
      <EmptyState
        title="That period was not found"
        message="Choose another archive period from the selector."
      />
    );
  }

  return (
    <main>
      <section className="hero-card archive-hero">
        <div>
          <p className="eyebrow">Archive</p>
          <h1>{archive.period}</h1>
          <p>Past battles, final standings, and the receipts.</p>
        </div>
        <form className="period-picker">
          <label htmlFor="period">Period</label>
          <select id="period" name="period" defaultValue={selectedPeriod}>
            {periods.map((period) => (
              <option key={period.period} value={period.period}>
                {period.period}
              </option>
            ))}
          </select>
          <button type="submit">View</button>
        </form>
      </section>

      <section className="metric-grid" aria-label="Archive statistics">
        <MetricCard
          label="Total distance"
          value={`${archive.summary.total_distance.toFixed(1)} km`}
          detail="Archived effort"
        />
        <MetricCard
          label="Total runs"
          value={archive.summary.total_runs.toLocaleString()}
          detail="Logged activities"
        />
        <MetricCard
          label="Average run"
          value={`${archive.summary.average_distance.toFixed(1)} km`}
          detail="Per activity"
        />
      </section>

      <HighlightStrip highlights={archive.highlights} />
      <TeamLeaderboard teams={archive.teams} />
      <IndividualLeaderboard individuals={archive.individuals} />
    </main>
  );
}

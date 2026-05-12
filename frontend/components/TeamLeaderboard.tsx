import { ProgressBar } from "@/components/ProgressBar";
import type { TeamStanding } from "@/types/api";

type TeamLeaderboardProps = {
  teams: TeamStanding[];
};

export function TeamLeaderboard({ teams }: TeamLeaderboardProps) {
  return (
    <section className="section-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Team race</p>
          <h2>Leaderboard</h2>
          <p className="section-sub">Distance for the current period</p>
        </div>
        <span>{teams.length} teams</span>
      </div>

      <div className="ranking-list">
        {teams.map((team) => (
          <article className="ranking-card" key={team.team}>
            <div className="rank-badge" style={{ borderColor: team.color }}>
              {team.medal ?? team.rank}
            </div>
            <div className="ranking-main">
              <div className="ranking-title-row">
                <div>
                  <h3>{team.team}</h3>
                  <p>{team.runners.join(", ")}</p>
                </div>
                <div className="team-distance-block">
                  <strong>{team.distance.toFixed(1)} km</strong>
                  {team.rank > 1 && (
                    <div className="team-gap-hints">
                      {team.distance_to_team_above != null &&
                        team.distance_to_team_above !== team.distance_to_leader && (
                          <span>{team.distance_to_team_above.toFixed(1)} km to next</span>
                        )}
                      <span>{team.distance_to_leader.toFixed(1)} km to lead</span>
                    </div>
                  )}
                </div>
              </div>
              <ProgressBar value={team.progress} color={team.color} />
              <div className="ranking-meta">
                <span>{team.member_count} runners</span>
                <span>{team.progress.toFixed(0)}% of leader</span>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

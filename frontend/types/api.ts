export type Summary = {
  total_distance: number;
  total_runs: number;
  average_distance: number;
  active_runners: number;
  active_teams: number;
  days_left: number;
};

export type TeamStanding = {
  rank: number;
  medal: string | null;
  team: string;
  distance: number;
  member_count: number;
  runners: string[];
  color: string;
  progress: number;
  distance_to_leader: number;
  distance_to_team_above: number | null;
};

export type IndividualStanding = {
  rank: number;
  medal: string | null;
  runner: string;
  team: string;
  distance: number;
  runs: number;
  streak_weeks: number;
  badges: string[];
  progress: number;
};

export type TeamContribution = {
  runner: string;
  distance: number;
  runs: number;
  progress: number;
};

export type Highlight = {
  label: string;
  value: string;
  detail: string;
};

export type CurrentChallengeResponse = {
  summary: Summary;
  teams: TeamStanding[];
  individuals: IndividualStanding[];
  contributions: Record<string, TeamContribution[]>;
  highlights: Highlight[];
};

export type ArchivePeriod = {
  period: string;
  label: string;
  total_distance: number;
  total_runs: number;
  active_runners: number;
  active_teams: number;
};

export type ArchivePeriodResponse = {
  period: string;
  summary: Summary;
  teams: TeamStanding[];
  individuals: IndividualStanding[];
  highlights: Highlight[];
};

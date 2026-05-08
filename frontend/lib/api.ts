import type {
  ArchivePeriod,
  ArchivePeriodResponse,
  CurrentChallengeResponse,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getCurrentChallenge() {
  return getJson<CurrentChallengeResponse>("/api/current");
}

export function getArchivePeriods() {
  return getJson<ArchivePeriod[]>("/api/archive/periods");
}

export function getArchivePeriod(period: string) {
  return getJson<ArchivePeriodResponse>(
    `/api/archive/${encodeURIComponent(period)}`,
  );
}

type BadgeCard = {
  name: string;
  description: string;
};

const stealableCrowns: BadgeCard[] = [
  {
    name: "67 King",
    description: "Own the most runs in the 6.65-6.75 km pocket this month and this crown stays on your head.",
  },
  {
    name: "Tenner Tyrant",
    description: "Stack the most runs between 9.5 and 10.5 km this month and rule the tenner zone.",
  },
  {
    name: "Long Haul Crown",
    description: "Log the most 15 km+ runs this month to take the long-distance throne.",
  },
];

const distanceVolumeBadges: BadgeCard[] = [
  {
    name: "69",
    description: "Hit any run from 6.85 to 6.95 km and this cheeky badge is yours.",
  },
  {
    name: "Palindrome",
    description: "Land within 0.05 km of 5.05, 6.06, 7.07, 8.08, or 9.09 and you unlock symmetry points.",
  },
  {
    name: "Century",
    description: "Crack 100 km in any calendar month and you earn this one.",
  },
  {
    name: "Double Century",
    description: "Push a month to 200 km or more and double up the flex.",
  },
  {
    name: "Ultra Engine",
    description: "Blast through 300 km in a month and your engine gets official status.",
  },
  {
    name: "Long Haul Lover",
    description: "Bag 3 or more runs of 15 km+ in one month and this one starts following you around.",
  },
  {
    name: "Mileage Monster",
    description: "Put up 75+ km in the current month and the monster wakes up.",
  },
  {
    name: "High Volume Machine",
    description: "Rack up 15 or more runs in a month and the machine badge turns on.",
  },
  {
    name: "Double Digits",
    description: "One run at 10 km or longer is all it takes to lock this in.",
  },
];

const consistencyPatternBadges: BadgeCard[] = [
  {
    name: "Consistency Club",
    description: "Clock at least 2 runs in each of the last 2 weeks of this month and you are officially dependable.",
  },
  {
    name: "Hat Trick",
    description: "Hit 3+ runs in each of the last 2 weeks of this month and you complete the weekly hat trick.",
  },
  {
    name: "Balanced Diet",
    description: "In one month, log a short run (<=5 km), a medium run (>5 and <10 km), and a long run (>=10 km).",
  },
  {
    name: "Streak Chef",
    description: "Stay active for at least 2 straight weeks this month with one or more runs each week.",
  },
  {
    name: "Perfect Month",
    description: "Finish a month with 4+ runs across at least 4 different active weeks.",
  },
  {
    name: "Double Duty",
    description: "Do at least 2 runs on the same day and this badge clocks your hustle.",
  },
  {
    name: "Podium Menace",
    description: "Sit in the top 3 of the individual leaderboard and keep the pressure on everyone else.",
  },
];

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

        <section className="badges-section">
          <h2>Distance &amp; Volume Badges</h2>
          <div className="badges-grid">
            {distanceVolumeBadges.map((badge) => (
              <article className="badge-card" key={badge.name}>
                <h3 className="badge-card__title">
                  <span className="soft-badge">{badge.name}</span>
                </h3>
                <p>{badge.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="badges-section">
          <h2>Consistency &amp; Patterns</h2>
          <div className="badges-grid">
            {consistencyPatternBadges.map((badge) => (
              <article className="badge-card" key={badge.name}>
                <h3 className="badge-card__title">
                  <span className="soft-badge">{badge.name}</span>
                </h3>
                <p>{badge.description}</p>
              </article>
            ))}
          </div>
        </section>
      </article>
    </main>
  );
}

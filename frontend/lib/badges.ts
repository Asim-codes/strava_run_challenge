export type BadgeDefinition = {
  name: string;
  description: string;
};

export type BadgeCategory = {
  title: string;
  badges: BadgeDefinition[];
};

export const stealableCrowns: BadgeDefinition[] = [
  {
    name: "67 King",
    description:
      "Own the most runs in the 6.65–6.75 km pocket this period and this crown stays on your head.",
  },
  {
    name: "Tenner Tyrant",
    description:
      "Stack the most runs between 9.5 and 10.5 km this period and rule the tenner zone.",
  },
  {
    name: "Long Haul Crown",
    description:
      "Log the most 15 km+ runs this period to take the long-distance throne.",
  },
];

export const earnedBadges: BadgeCategory[] = [
  {
    title: "Distance Milestones",
    badges: [
      {
        name: "Ultra Engine",
        description: "Hit 300 km in the current period. Absolute machine.",
      },
      {
        name: "Double Century",
        description: "Crack 200 km in the current period and double up the flex.",
      },
      {
        name: "Century Club",
        description: "Rack up 100 km in the current period to earn membership.",
      },
      {
        name: "Mileage Monster",
        description: "Put up 75+ km in the current period and the monster wakes up.",
      },
      {
        name: "Double Digits",
        description: "One run at 10 km or longer is all it takes to lock this in.",
      },
    ],
  },
  {
    title: "Volume",
    badges: [
      {
        name: "High Volume Machine",
        description:
          "Log 15 or more runs of 5 km or above in the current period and the machine badge turns on.",
      },
    ],
  },
  {
    title: "Consistency & Patterns",
    badges: [
      {
        name: "Consistency Club",
        description:
          "Log 2+ runs of 5 km or more in the last completed week. Miss it the next week and it's gone.",
      },
      {
        name: "Hat Trick",
        description:
          "Hit 3+ runs of 5 km or more in any single week within the period.",
      },
      {
        name: "Streak Chef",
        description:
          "Stay active for at least 2 straight weeks with one or more runs each week.",
      },
      {
        name: "Perfect Month",
        description:
          "Finish a calendar month with 4+ runs across at least 4 different active weeks.",
      },
      {
        name: "Palindrome",
        description:
          "Land within 0.05 km of 5.05, 6.06, 7.07, 8.08, or 9.09 and unlock symmetry points.",
      },
      {
        name: "Balanced Diet",
        description:
          "Log at least one run in each tier — 5–9 km, 10–14 km, and 15 km+ — in the current period.",
      },
      {
        name: "Podium Menace",
        description:
          "Sit in the top 3 of the individual leaderboard and keep the pressure on everyone else.",
      },
    ],
  },
];

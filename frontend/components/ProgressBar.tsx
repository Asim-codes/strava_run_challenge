type ProgressBarProps = {
  value: number;
  color?: string;
};

export function ProgressBar({ value, color = "#f97316" }: ProgressBarProps) {
  return (
    <div className="progress-track" aria-label={`${value}% of leader distance`}>
      <div
        className="progress-fill"
        style={{ width: `${Math.min(value, 100)}%`, background: color }}
      />
    </div>
  );
}

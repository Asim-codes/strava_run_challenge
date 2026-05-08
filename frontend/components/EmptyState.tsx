type EmptyStateProps = {
  title: string;
  message: string;
};

export function EmptyState({ title, message }: EmptyStateProps) {
  return (
    <section className="empty-state">
      <p className="eyebrow">Not ready yet</p>
      <h2>{title}</h2>
      <p>{message}</p>
    </section>
  );
}

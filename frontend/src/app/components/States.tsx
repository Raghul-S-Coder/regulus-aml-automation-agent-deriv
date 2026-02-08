type StateProps = {
  title: string;
  message?: string;
};

export function LoadingState({ title, message }: StateProps) {
  return (
    <div className="rounded-2xl border border-border bg-surface-secondary p-6">
      <p className="text-sm font-semibold text-text">{title}</p>
      <p className="mt-2 text-sm text-text-muted">{message ?? "Loading data..."}</p>
      <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-surface">
        <div className="h-full w-1/3 animate-pulse rounded-full bg-brand/60" />
      </div>
    </div>
  );
}

export function ErrorState({ title, message }: StateProps) {
  return (
    <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 p-6">
      <p className="text-sm font-semibold text-rose-700">{title}</p>
      <p className="mt-2 text-sm text-rose-700/80">{message ?? "Something went wrong."}</p>
    </div>
  );
}

export function EmptyState({ title, message }: StateProps) {
  return (
    <div className="rounded-2xl border border-border bg-surface-secondary p-6 text-center">
      <p className="text-sm font-semibold text-text">{title}</p>
      <p className="mt-2 text-sm text-text-muted">{message ?? "No records found."}</p>
    </div>
  );
}

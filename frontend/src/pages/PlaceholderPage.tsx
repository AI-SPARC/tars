export function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="rounded-2xl border bg-card/80 p-8">
      <h1 className="m-0 text-4xl tracking-[-0.05em]">{title}</h1>
      <p className="mb-0 mt-3 text-muted-foreground">This operator page is planned for the next MVP phase.</p>
    </div>
  );
}

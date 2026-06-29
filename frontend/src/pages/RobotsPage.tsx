import { RobotTable } from '../components/robots/RobotTable';
import { Badge } from '../components/ui/badge';
import { useRobots } from '../hooks/useRobots';

export function RobotsPage() {
  const robots = useRobots();

  return (
    <div className="grid gap-8">
      <header>
        <Badge className="mb-4 uppercase tracking-[0.14em]" variant="outline">
          Fleet registry
        </Badge>
        <h1 className="m-0 text-5xl tracking-[-0.06em]">Robots</h1>
        <p className="mt-3 text-muted-foreground">
          Robots discovered through MQTT or registered through the fleet API.
        </p>
      </header>
      {robots.isLoading && (
        <div aria-label="Loading robots" className="h-64 animate-pulse rounded-2xl border bg-card" />
      )}
      {robots.isError && (
        <div className="rounded-xl border bg-card px-4 py-3 text-sm" role="alert">
          Fleet data could not be loaded: {robots.error.message}
        </div>
      )}
      {!robots.isLoading && <RobotTable robots={robots.data ?? []} />}
    </div>
  );
}

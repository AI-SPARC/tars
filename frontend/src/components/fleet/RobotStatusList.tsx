import type { Robot } from '../../api/client';
import { Badge } from '../ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export function RobotStatusList({ robots }: { robots: Robot[] }) {
  return (
    <Card className="min-h-[320px] rounded-2xl bg-card/80 shadow-none">
      <CardHeader className="flex-row items-start justify-between space-y-0">
        <div>
          <CardTitle className="text-lg tracking-[-0.03em]">Fleet status</CardTitle>
          <CardDescription className="mt-1">Latest connection state by robot</CardDescription>
        </div>
        <a className="text-xs font-semibold underline-offset-4 hover:underline" href="/robots">
          View fleet
        </a>
      </CardHeader>
      <CardContent>
        {robots.length === 0 ? (
          <EmptyState message="No robots discovered yet." />
        ) : (
          <ul className="m-0 grid list-none gap-1 p-0">
            {robots.slice(0, 6).map((robot) => {
              const online = robot.lastConnectionState === 'ONLINE';
              return (
                <li
                  className="flex items-center justify-between border-b py-3 last:border-b-0"
                  key={robot.id}
                >
                  <div className="min-w-0">
                    <strong className="block truncate text-sm font-medium">
                      {robot.displayName || robot.serialNumber}
                    </strong>
                    <span className="text-xs text-muted-foreground">
                      {robot.manufacturer} · {robot.serialNumber}
                    </span>
                  </div>
                  <Badge variant={online ? 'default' : 'outline'}>{robot.lastConnectionState}</Badge>
                </li>
              );
            })}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="grid min-h-48 place-items-center rounded-xl border border-dashed text-sm text-muted-foreground">
      {message}
    </div>
  );
}

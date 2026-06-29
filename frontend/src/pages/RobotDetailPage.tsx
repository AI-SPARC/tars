import { Link, useParams } from '@tanstack/react-router';

import { JsonPanel, RobotStatePanel } from '../components/robots/RobotStatePanel';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { useCancelOrder, useRobot, useRobotFactsheet, useRobotState } from '../hooks/useRobots';

export function RobotDetailPage() {
  const { robotId } = useParams({ from: '/robots/$robotId' });
  const robot = useRobot(robotId);
  const state = useRobotState(robotId);
  const factsheet = useRobotFactsheet(robotId);
  const cancelOrder = useCancelOrder(robotId);

  const handleCancelOrder = () => {
    if (window.confirm('Send cancelOrder to this robot?')) cancelOrder.mutate();
  };

  if (robot.isLoading) {
    return <div aria-label="Loading robot" className="h-80 animate-pulse rounded-2xl border bg-card" />;
  }
  if (robot.isError || !robot.data) {
    return (
      <div className="rounded-xl border bg-card p-5" role="alert">
        Robot could not be loaded. <Link to="/robots">Return to fleet</Link>
      </div>
    );
  }

  return (
    <div className="grid gap-7">
      <header className="flex items-end justify-between gap-6">
        <div>
          <Link className="text-xs font-semibold text-muted-foreground hover:underline" to="/robots">
            ← Fleet registry
          </Link>
          <h1 className="mb-2 mt-4 text-5xl tracking-[-0.06em]">
            {robot.data.displayName || robot.data.serialNumber}
          </h1>
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <span>{robot.data.manufacturer}</span>
            <span>·</span>
            <span>{robot.data.serialNumber}</span>
            <Badge variant={robot.data.lastConnectionState === 'ONLINE' ? 'default' : 'outline'}>
              {robot.data.lastConnectionState}
            </Badge>
          </div>
        </div>
        <Button disabled={cancelOrder.isPending} onClick={handleCancelOrder} variant="outline">
          {cancelOrder.isPending ? 'Sending…' : 'Cancel current order'}
        </Button>
      </header>

      {cancelOrder.isSuccess && (
        <div className="rounded-xl border bg-card px-4 py-3 text-sm" role="status">
          cancelOrder was published to the robot.
        </div>
      )}
      {cancelOrder.isError && (
        <div className="rounded-xl border bg-card px-4 py-3 text-sm" role="alert">
          cancelOrder could not be published: {cancelOrder.error.message}
        </div>
      )}

      <RobotStatePanel state={state.data} />
      <Card className="rounded-2xl bg-card/80 shadow-none">
        <CardHeader>
          <CardTitle className="text-lg">Factsheet</CardTitle>
          <CardDescription>Robot capabilities and protocol limits</CardDescription>
        </CardHeader>
        <CardContent>
          {factsheet.data ? (
            <JsonPanel value={factsheet.data} />
          ) : (
            <p className="m-0 text-sm text-muted-foreground">No factsheet has been received.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

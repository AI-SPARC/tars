import type { RobotState } from '../../api/client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export function RobotStatePanel({ state }: { state: RobotState | undefined }) {
  if (!state) {
    return (
      <Card className="rounded-2xl bg-card/80 shadow-none">
        <CardHeader>
          <CardTitle className="text-lg">Latest state</CardTitle>
          <CardDescription>No state message has been received for this robot.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  const metrics = [
    ['Battery', state.batteryCharge == null ? '—' : `${state.batteryCharge}%`],
    ['Mode', state.operatingMode ?? '—'],
    ['Last node', state.lastNodeId || '—'],
    ['Order', state.orderId || '—'],
  ];
  return (
    <Card className="rounded-2xl bg-card/80 shadow-none">
      <CardHeader>
        <CardTitle className="text-lg">Latest state</CardTitle>
        <CardDescription>Most recent validated VDA 5050 state snapshot</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-5">
        <dl className="grid grid-cols-4 gap-3">
          {metrics.map(([label, value]) => (
            <div className="rounded-xl border bg-background p-3" key={label}>
              <dt className="text-[0.67rem] font-bold uppercase tracking-[0.12em] text-muted-foreground">
                {label}
              </dt>
              <dd className="m-0 mt-2 truncate text-sm font-semibold">{value}</dd>
            </div>
          ))}
        </dl>
        <JsonPanel value={state.rawPayload ?? state} />
      </CardContent>
    </Card>
  );
}

export function JsonPanel({ value }: { value: unknown }) {
  return (
    <pre className="m-0 max-h-80 overflow-auto rounded-xl bg-neutral-950 p-4 text-xs leading-5 text-neutral-100">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

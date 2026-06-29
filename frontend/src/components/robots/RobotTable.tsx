import { Link } from '@tanstack/react-router';

import type { Robot } from '../../api/client';
import { Badge } from '../ui/badge';

export function RobotTable({ robots }: { robots: Robot[] }) {
  if (robots.length === 0) {
    return (
      <div className="grid min-h-64 place-items-center rounded-2xl border border-dashed bg-card/60 text-sm text-muted-foreground">
        No robots discovered. Publish a VDA 5050 connection message to register one.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border bg-card/80">
      <table className="w-full border-collapse text-left text-sm">
        <thead className="border-b bg-muted/60 text-[0.68rem] uppercase tracking-[0.13em] text-muted-foreground">
          <tr>
            <th className="px-5 py-4 font-bold">Robot</th>
            <th className="px-5 py-4 font-bold">Manufacturer</th>
            <th className="px-5 py-4 font-bold">Protocol</th>
            <th className="px-5 py-4 font-bold">Connection</th>
            <th className="px-5 py-4 text-right font-bold">Details</th>
          </tr>
        </thead>
        <tbody>
          {robots.map((robot) => (
            <tr className="border-b last:border-b-0" key={robot.id}>
              <td className="px-5 py-4">
                <strong className="block font-medium">{robot.displayName || robot.serialNumber}</strong>
                <span className="text-xs text-muted-foreground">{robot.serialNumber}</span>
              </td>
              <td className="px-5 py-4">{robot.manufacturer}</td>
              <td className="px-5 py-4 font-mono text-xs">{robot.protocolVersion}</td>
              <td className="px-5 py-4">
                <Badge variant={robot.lastConnectionState === 'ONLINE' ? 'default' : 'outline'}>
                  {robot.lastConnectionState}
                </Badge>
              </td>
              <td className="px-5 py-4 text-right">
                <Link
                  className="font-semibold underline-offset-4 hover:underline"
                  params={{ robotId: robot.id }}
                  to="/robots/$robotId"
                >
                  Open
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

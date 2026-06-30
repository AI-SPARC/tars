import { Bot, CircleAlert, Map, Route } from 'lucide-react';
import type { ComponentType } from 'react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export type FleetSummary = {
  robots: number;
  onlineRobots: number;
  activeMissions: number;
  maps: number;
  protocolErrors: number;
};

type Metric = {
  label: string;
  value: number;
  detail: string;
  icon: ComponentType<{ size?: number; strokeWidth?: number }>;
};

export function FleetSummaryCards({ summary }: { summary: FleetSummary }) {
  const metrics: Metric[] = [
    {
      label: 'Fleet',
      value: summary.robots,
      detail: `${summary.onlineRobots} online`,
      icon: Bot,
    },
    {
      label: 'Active missions',
      value: summary.activeMissions,
      detail: 'Queued through running',
      icon: Route,
    },
    {
      label: 'Graph maps',
      value: summary.maps,
      detail: 'Available for routing',
      icon: Map,
    },
    {
      label: 'VDA errors',
      value: summary.protocolErrors,
      detail: 'Invalid persisted messages',
      icon: CircleAlert,
    },
  ];

  return (
    <section aria-label="Fleet summary" className="grid grid-cols-4 gap-3.5">
      {metrics.map((metric) => {
        const Icon = metric.icon;
        return (
          <Card className="rounded-2xl bg-card/80 shadow-none" key={metric.label}>
            <CardHeader className="flex-row items-center justify-between space-y-0 pb-3">
              <CardDescription className="text-[0.69rem] font-bold uppercase tracking-[0.14em]">
                {metric.label}
              </CardDescription>
              <Icon size={17} strokeWidth={1.7} />
            </CardHeader>
            <CardContent>
              <CardTitle className="text-4xl tracking-[-0.06em]">{metric.value}</CardTitle>
              <CardDescription className="mt-2">{metric.detail}</CardDescription>
            </CardContent>
          </Card>
        );
      })}
    </section>
  );
}

import { FleetSummaryCards } from '../components/fleet/FleetSummaryCards';
import { RobotStatusList } from '../components/fleet/RobotStatusList';
import { RecentMessages } from '../components/mqtt/RecentMessages';
import { Badge } from '../components/ui/badge';
import { useMaps } from '../hooks/useMaps';
import { useMissions } from '../hooks/useMissions';
import { useMqttMessages } from '../hooks/useMqttMessages';
import { useRobots } from '../hooks/useRobots';

const activeMissionStatuses = new Set(['queued', 'assigned', 'sent', 'running']);

export function DashboardPage() {
  const robots = useRobots();
  const missions = useMissions();
  const maps = useMaps();
  const recentMessages = useMqttMessages({ pageSize: 6 });
  const invalidMessages = useMqttMessages({ schemaValid: false, pageSize: 1 });
  const loading = [robots, missions, maps, recentMessages, invalidMessages].some(
    (query) => query.isLoading,
  );
  const error = [robots, missions, maps, recentMessages, invalidMessages].find(
    (query) => query.isError,
  )?.error;
  const robotData = robots.data ?? [];
  const missionData = missions.data ?? [];

  return (
    <div className="grid gap-8">
      <section className="flex items-end justify-between gap-8">
        <div>
          <Badge className="mb-4 rounded-md px-2 text-[0.68rem] uppercase tracking-[0.16em]" variant="outline">
            Live operations
          </Badge>
          <h1 className="m-0 text-[clamp(2.8rem,5vw,5.5rem)] leading-[0.92] tracking-[-0.075em]">
            Fleet overview.
          </h1>
          <p className="mt-4 max-w-[650px] text-base leading-7 text-neutral-700">
            Current robot connectivity, mission workload, graph maps, and VDA 5050 traffic.
          </p>
        </div>
        <div className="pb-2 text-right text-xs text-muted-foreground">
          <span className="block font-bold uppercase tracking-[0.14em] text-foreground">
            Live cache
          </span>
          <span>Updated by WebSocket events</span>
        </div>
      </section>

      {error && (
        <div className="rounded-xl border bg-card px-4 py-3 text-sm" role="alert">
          Dashboard data could not be loaded: {error instanceof Error ? error.message : 'Unknown error'}
        </div>
      )}

      {loading ? (
        <DashboardLoading />
      ) : (
        <>
          <FleetSummaryCards
            summary={{
              robots: robotData.length,
              onlineRobots: robotData.filter((robot) => robot.lastConnectionState === 'ONLINE').length,
              activeMissions: missionData.filter((mission) => activeMissionStatuses.has(mission.status)).length,
              maps: maps.data?.length ?? 0,
              protocolErrors: invalidMessages.data?.total ?? 0,
            }}
          />
          <section className="grid grid-cols-2 gap-3.5">
            <RobotStatusList robots={robotData} />
            <RecentMessages messages={recentMessages.data?.items ?? []} />
          </section>
        </>
      )}
    </div>
  );
}

function DashboardLoading() {
  return (
    <div aria-label="Loading dashboard" className="grid gap-4">
      <div className="grid grid-cols-4 gap-3.5">
        {[0, 1, 2, 3].map((item) => (
          <div className="h-40 animate-pulse rounded-2xl border bg-card" key={item} />
        ))}
      </div>
      <div className="grid grid-cols-2 gap-3.5">
        <div className="h-80 animate-pulse rounded-2xl border bg-card" />
        <div className="h-80 animate-pulse rounded-2xl border bg-card" />
      </div>
    </div>
  );
}

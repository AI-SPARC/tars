import { useEffect, useState } from 'react';

import { MissionForm } from '../components/missions/MissionForm';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { useMap, useMaps, useRoutePreview } from '../hooks/useMaps';
import { useCreateMission } from '../hooks/useMissions';
import { useRobots } from '../hooks/useRobots';

export function MissionBuilderPage() {
  const maps = useMaps();
  const robots = useRobots();
  const [selectedMapId, setSelectedMapId] = useState('');
  const map = useMap(selectedMapId || undefined);
  const routePreview = useRoutePreview(selectedMapId || undefined);
  const createMission = useCreateMission();

  useEffect(() => {
    if (!selectedMapId && maps.data?.[0]) setSelectedMapId(maps.data[0].id);
  }, [maps.data, selectedMapId]);

  return (
    <Card className="rounded-2xl bg-card/80 shadow-none">
      <CardHeader>
        <CardTitle className="text-lg">Mission builder</CardTitle>
        <CardDescription>Create an assigned point-to-point mission on a graph map.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        <MissionForm
          busy={createMission.isPending || routePreview.isPending}
          maps={maps.data ?? []}
          nodes={map.data?.nodes ?? []}
          onMapChange={(mapId) => {
            setSelectedMapId(mapId);
            routePreview.reset();
          }}
          onPreview={(startNodeKey, goalNodeKey) =>
            routePreview.mutate({ startNodeKey, goalNodeKey })
          }
          onSubmit={(input) => createMission.mutateAsync(input)}
          robots={robots.data ?? []}
          route={routePreview.data?.nodeKeys}
          selectedMapId={selectedMapId}
        />
        {createMission.isSuccess && (
          <div className="rounded-xl border bg-background p-3 text-sm" role="status">
            Mission {createMission.data.id} created with status {createMission.data.status}.
          </div>
        )}
        {(createMission.isError || routePreview.isError) && (
          <div className="rounded-xl border bg-background p-3 text-sm" role="alert">
            {createMission.error?.message || routePreview.error?.message}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

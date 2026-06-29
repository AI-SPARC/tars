import { useEffect, useMemo, useState, type FormEvent } from 'react';

import { EdgeEditor } from '../components/map/EdgeEditor';
import { MapGraph } from '../components/map/MapGraph';
import { NodeEditor } from '../components/map/NodeEditor';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  useAddMapEdge,
  useAddMapNode,
  useCreateMap,
  useMap,
  useMaps,
  useRoutePreview,
} from '../hooks/useMaps';
import { useRobots, useRobotStates } from '../hooks/useRobots';

export function MapPage() {
  const maps = useMaps();
  const [selectedMapId, setSelectedMapId] = useState<string>();
  const map = useMap(selectedMapId);
  const robots = useRobots();
  const robotStates = useRobotStates((robots.data ?? []).map((robot) => robot.id));
  const createMap = useCreateMap();
  const addNode = useAddMapNode(selectedMapId);
  const addEdge = useAddMapEdge(selectedMapId);
  const routePreview = useRoutePreview(selectedMapId);

  useEffect(() => {
    if (!selectedMapId && maps.data?.[0]) setSelectedMapId(maps.data[0].id);
  }, [maps.data, selectedMapId]);

  const robotPositions = useMemo(
    () =>
      (robots.data ?? []).flatMap((robot, index) => {
        const state = robotStates[index]?.data;
        return state ? [{ robot, state }] : [];
      }),
    [robotStates, robots.data],
  );

  return (
    <div className="grid gap-7">
      <header className="flex items-end justify-between gap-6">
        <div>
          <Badge className="mb-4 uppercase tracking-[0.14em]" variant="outline">Graph workspace</Badge>
          <h1 className="m-0 text-5xl tracking-[-0.06em]">Map & Routes</h1>
          <p className="mb-0 mt-3 text-muted-foreground">Build a directed weighted graph and inspect robot positions.</p>
        </div>
        <select className="h-10 min-w-56 rounded-md border bg-card px-3 text-sm" onChange={(event) => setSelectedMapId(event.target.value || undefined)} value={selectedMapId ?? ''}>
          <option value="">Select a map</option>
          {(maps.data ?? []).map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
      </header>

      <CreateMapForm disabled={createMap.isPending} onSubmit={async (name) => {
        const created = await createMap.mutateAsync({ name });
        setSelectedMapId(created.id);
      }} />

      {map.data ? (
        <>
          <section className="grid grid-cols-[minmax(0,1fr)_280px] gap-4">
            <MapGraph map={map.data} robots={robotPositions} highlightedNodeKeys={routePreview.data?.nodeKeys} />
            <Card className="rounded-2xl bg-card/80 shadow-none">
              <CardHeader><CardTitle className="text-lg">Graph editor</CardTitle></CardHeader>
              <CardContent className="grid gap-7">
                <NodeEditor disabled={addNode.isPending} onSubmit={(input) => addNode.mutateAsync(input)} />
                <EdgeEditor disabled={addEdge.isPending} nodes={map.data.nodes} onSubmit={(input) => addEdge.mutateAsync(input)} />
              </CardContent>
            </Card>
          </section>
          <RoutePreviewForm
            disabled={routePreview.isPending}
            nodes={map.data.nodes.map((node) => node.nodeKey)}
            onSubmit={(startNodeKey, goalNodeKey) => routePreview.mutate({ startNodeKey, goalNodeKey })}
            result={routePreview.data?.nodeKeys}
          />
        </>
      ) : (
        <div className="grid h-80 place-items-center rounded-2xl border border-dashed bg-card/60 text-sm text-muted-foreground">
          Create or select a map to open the graph editor.
        </div>
      )}
    </div>
  );
}

function CreateMapForm({ disabled, onSubmit }: { disabled: boolean; onSubmit: (name: string) => Promise<unknown> }) {
  const [name, setName] = useState('');
  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit(name.trim());
    setName('');
  };
  return (
    <form className="flex items-end gap-3 rounded-2xl border bg-card/80 p-4" onSubmit={submit}>
      <label className="grid flex-1 gap-1 text-xs font-medium">New map name<input className="h-9 rounded-md border bg-background px-3" onChange={(event) => setName(event.target.value)} required value={name} /></label>
      <Button disabled={disabled} size="sm" type="submit">Create map</Button>
    </form>
  );
}

function RoutePreviewForm({ nodes, disabled, onSubmit, result }: { nodes: string[]; disabled: boolean; onSubmit: (start: string, goal: string) => void; result?: string[] }) {
  const [start, setStart] = useState('');
  const [goal, setGoal] = useState('');
  useEffect(() => {
    if (!start && nodes[0]) setStart(nodes[0]);
    if (!goal && nodes[1]) setGoal(nodes[1]);
  }, [goal, nodes, start]);
  return (
    <Card className="rounded-2xl bg-card/80 shadow-none">
      <CardContent className="flex items-end gap-3 pt-6">
        <RouteSelect label="Start" nodes={nodes} onChange={setStart} value={start} />
        <RouteSelect label="Goal" nodes={nodes} onChange={setGoal} value={goal} />
        <Button disabled={disabled || !start || !goal} onClick={() => onSubmit(start, goal)} size="sm">Preview route</Button>
        <span className="ml-auto text-sm text-muted-foreground">{result?.join(' → ') || 'No route preview'}</span>
      </CardContent>
    </Card>
  );
}

function RouteSelect({ label, nodes, onChange, value }: { label: string; nodes: string[]; onChange: (value: string) => void; value: string }) {
  return <label className="grid gap-1 text-xs font-medium">{label}<select className="h-9 min-w-40 rounded-md border bg-background px-2" onChange={(event) => onChange(event.target.value)} value={value}><option value="">Select</option>{nodes.map((node) => <option key={node} value={node}>{node}</option>)}</select></label>;
}

import { useState, type FormEvent, type ReactNode } from 'react';

import type { FleetMap, MapNode, MissionInput, Robot } from '../../api/client';
import { Button } from '../ui/button';

export function MissionForm({
  maps,
  robots,
  nodes,
  selectedMapId,
  busy,
  route,
  onMapChange,
  onPreview,
  onSubmit,
}: {
  maps: FleetMap[];
  robots: Robot[];
  nodes: MapNode[];
  selectedMapId: string;
  busy: boolean;
  route?: string[];
  onMapChange: (mapId: string) => void;
  onPreview: (startNodeKey: string, goalNodeKey: string) => void;
  onSubmit: (input: MissionInput) => Promise<unknown>;
}) {
  const [robotId, setRobotId] = useState('');
  const [startNodeKey, setStartNodeKey] = useState('');
  const [goalNodeKey, setGoalNodeKey] = useState('');
  const [priority, setPriority] = useState('0');

  const resolvedRobotId = robots.some((robot) => robot.id === robotId)
    ? robotId
    : robots[0]?.id ?? '';
  const resolvedStartNodeKey = nodes.some((node) => node.nodeKey === startNodeKey)
    ? startNodeKey
    : nodes[0]?.nodeKey ?? '';
  const resolvedGoalNodeKey = nodes.some((node) => node.nodeKey === goalNodeKey)
    ? goalNodeKey
    : nodes[1]?.nodeKey ?? nodes[0]?.nodeKey ?? '';

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit({
      mapId: selectedMapId,
      assignedRobotId: resolvedRobotId,
      startNodeKey: resolvedStartNodeKey,
      goalNodeKey: resolvedGoalNodeKey,
      priority: Number(priority),
    });
  };
  const ready = Boolean(
    selectedMapId && resolvedRobotId && resolvedStartNodeKey && resolvedGoalNodeKey,
  );

  return (
    <form className="grid gap-4" onSubmit={submit}>
      <Field label="Map">
        <select onChange={(event) => onMapChange(event.target.value)} required value={selectedMapId}>
          <option value="">Select a map</option>
          {maps.map((map) => <option key={map.id} value={map.id}>{map.name}</option>)}
        </select>
      </Field>
      <Field label="Robot">
        <select onChange={(event) => setRobotId(event.target.value)} required value={resolvedRobotId}>
          <option value="">Select a robot</option>
          {robots.map((robot) => <option key={robot.id} value={robot.id}>{robot.displayName || robot.serialNumber}</option>)}
        </select>
      </Field>
      <div className="grid grid-cols-2 gap-3">
        <Field label="Start node">
          <select onChange={(event) => setStartNodeKey(event.target.value)} required value={resolvedStartNodeKey}>
            <option value="">Select</option>
            {nodes.map((node) => <option key={node.id} value={node.nodeKey}>{node.nodeKey}</option>)}
          </select>
        </Field>
        <Field label="Goal node">
          <select onChange={(event) => setGoalNodeKey(event.target.value)} required value={resolvedGoalNodeKey}>
            <option value="">Select</option>
            {nodes.map((node) => <option key={node.id} value={node.nodeKey}>{node.nodeKey}</option>)}
          </select>
        </Field>
      </div>
      <Field label="Priority">
        <input min="0" onChange={(event) => setPriority(event.target.value)} type="number" value={priority} />
      </Field>
      <div className="rounded-xl border bg-background p-3 text-xs text-muted-foreground">
        {route?.length ? route.join(' → ') : 'Preview the route before creating the mission.'}
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Button disabled={!ready || busy} onClick={() => onPreview(resolvedStartNodeKey, resolvedGoalNodeKey)} type="button" variant="outline">
          Preview route
        </Button>
        <Button disabled={!ready || busy} type="submit">Create mission</Button>
      </div>
    </form>
  );
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="grid gap-1 text-xs font-medium [&_input]:h-9 [&_input]:rounded-md [&_input]:border [&_input]:bg-background [&_input]:px-3 [&_select]:h-9 [&_select]:min-w-0 [&_select]:rounded-md [&_select]:border [&_select]:bg-background [&_select]:px-2">
      {label}
      {children}
    </label>
  );
}

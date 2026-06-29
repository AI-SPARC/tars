import { useEffect, useState, type FormEvent } from 'react';

import type { MapEdgeInput, MapNode } from '../../api/client';
import { Button } from '../ui/button';

export function EdgeEditor({
  nodes,
  disabled,
  onSubmit,
}: {
  nodes: MapNode[];
  disabled?: boolean;
  onSubmit: (edge: MapEdgeInput) => Promise<unknown>;
}) {
  const [edgeKey, setEdgeKey] = useState('');
  const [fromNodeKey, setFromNodeKey] = useState('');
  const [toNodeKey, setToNodeKey] = useState('');
  const [distance, setDistance] = useState('1');
  const [bidirectional, setBidirectional] = useState(false);

  useEffect(() => {
    if (!fromNodeKey && nodes[0]) setFromNodeKey(nodes[0].nodeKey);
    if (!toNodeKey && nodes[1]) setToNodeKey(nodes[1].nodeKey);
  }, [fromNodeKey, nodes, toNodeKey]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onSubmit({
      edgeKey: edgeKey.trim(),
      fromNodeKey,
      toNodeKey,
      distance: Number(distance),
      bidirectional,
    });
    setEdgeKey('');
  };

  return (
    <form className="grid gap-3" onSubmit={submit}>
      <h3 className="m-0 text-sm font-semibold">Add edge</h3>
      <label className="grid gap-1 text-xs font-medium">
        Edge ID
        <input className="h-9 rounded-md border bg-background px-3" onChange={(event) => setEdgeKey(event.target.value)} required value={edgeKey} />
      </label>
      <div className="grid grid-cols-2 gap-2">
        <NodeSelect label="From" nodes={nodes} onChange={setFromNodeKey} value={fromNodeKey} />
        <NodeSelect label="To" nodes={nodes} onChange={setToNodeKey} value={toNodeKey} />
      </div>
      <label className="grid gap-1 text-xs font-medium">
        Distance
        <input className="h-9 rounded-md border bg-background px-3" min="0" onChange={(event) => setDistance(event.target.value)} required step="any" type="number" value={distance} />
      </label>
      <label className="flex items-center gap-2 text-xs font-medium">
        <input checked={bidirectional} onChange={(event) => setBidirectional(event.target.checked)} type="checkbox" />
        Bidirectional
      </label>
      <Button disabled={disabled || nodes.length < 2} size="sm" type="submit">Save edge</Button>
    </form>
  );
}

function NodeSelect({ label, nodes, onChange, value }: { label: string; nodes: MapNode[]; onChange: (value: string) => void; value: string }) {
  return (
    <label className="grid gap-1 text-xs font-medium">
      {label}
      <select className="h-9 min-w-0 rounded-md border bg-background px-2" onChange={(event) => onChange(event.target.value)} required value={value}>
        <option value="">Select</option>
        {nodes.map((node) => <option key={node.id} value={node.nodeKey}>{node.nodeKey}</option>)}
      </select>
    </label>
  );
}

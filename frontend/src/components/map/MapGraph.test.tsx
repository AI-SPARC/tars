import '@testing-library/jest-dom/vitest';

import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { EdgeEditor } from './EdgeEditor';
import { MapGraph } from './MapGraph';
import { NodeEditor } from './NodeEditor';

const nodes = [
  { id: 'node-a', nodeKey: 'A', x: 0, y: 0, theta: 0, nodeType: 'waypoint' },
  { id: 'node-b', nodeKey: 'B', x: 5, y: 2, theta: 0, nodeType: 'waypoint' },
];

describe('map graph workspace', () => {
  it('renders nodes, directed edges, highlighted route, and robot position', () => {
    const { container } = render(
      <MapGraph
        highlightedNodeKeys={['A', 'B']}
        map={{
          id: 'map-1',
          name: 'Lab',
          description: null,
          nodes,
          edges: [
            {
              id: 'edge-a-b',
              edgeKey: 'A-B',
              fromNodeKey: 'A',
              toNodeKey: 'B',
              distance: 5.4,
              bidirectional: false,
            },
          ],
        }}
        robots={[
          {
            robot: {
              id: 'robot-1',
              manufacturer: 'ResearchBot',
              serialNumber: 'RB001',
              displayName: 'Picker',
              protocolVersion: '3.0.0',
              lastConnectionState: 'ONLINE',
            },
            state: { agvPosition: { x: 2, y: 1, mapId: 'map-1' } },
          },
        ]}
      />,
    );

    expect(screen.getByRole('img', { name: 'Graph map Lab' })).toBeInTheDocument();
    expect(container.querySelectorAll('[data-node-key]')).toHaveLength(2);
    expect(container.querySelector('[data-edge-key="A-B"]')).toHaveAttribute('stroke', '#111');
    expect(container.querySelector('[data-robot-id="robot-1"]')).toBeInTheDocument();
    expect(screen.getByText('Picker')).toBeInTheDocument();
  });

  it('submits node and edge editor values', async () => {
    const addNode = vi.fn().mockResolvedValue(undefined);
    const addEdge = vi.fn().mockResolvedValue(undefined);
    const { rerender } = render(<NodeEditor onSubmit={addNode} />);

    fireEvent.change(screen.getByLabelText('Node ID'), { target: { value: 'C' } });
    fireEvent.change(screen.getByLabelText('X'), { target: { value: '3.5' } });
    fireEvent.change(screen.getByLabelText('Y'), { target: { value: '4' } });
    fireEvent.click(screen.getByRole('button', { name: 'Save node' }));
    await waitFor(() =>
      expect(addNode).toHaveBeenCalledWith({ nodeKey: 'C', x: 3.5, y: 4, theta: 0 }),
    );

    rerender(<EdgeEditor nodes={nodes} onSubmit={addEdge} />);
    fireEvent.change(screen.getByLabelText('Edge ID'), { target: { value: 'A-B' } });
    fireEvent.click(screen.getByLabelText('Bidirectional'));
    fireEvent.click(screen.getByRole('button', { name: 'Save edge' }));
    await waitFor(() =>
      expect(addEdge).toHaveBeenCalledWith({
        edgeKey: 'A-B',
        fromNodeKey: 'A',
        toNodeKey: 'B',
        distance: 1,
        bidirectional: true,
      }),
    );
  });
});

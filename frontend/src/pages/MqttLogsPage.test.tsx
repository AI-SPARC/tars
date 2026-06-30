import '@testing-library/jest-dom/vitest';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createMemoryHistory, createRouter, RouterProvider } from '@tanstack/react-router';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '../api/client';
import { routeTree } from '../app/router';

class FakeWebSocket {
  addEventListener() {}
  close() {}
}

describe('MqttLogsPage', () => {
  beforeEach(() => {
    vi.stubGlobal('WebSocket', FakeWebSocket);
    vi.stubGlobal('scrollTo', vi.fn());
    vi.spyOn(apiClient, 'listRobots').mockResolvedValue([
      {
        id: 'robot-1',
        manufacturer: 'ResearchBot',
        serialNumber: 'RB001',
        displayName: 'Picker',
        protocolVersion: '3.0.0',
        lastConnectionState: 'ONLINE',
      },
    ]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('filters, paginates, and inspects validation errors and JSON payload', async () => {
    const listMessages = vi.spyOn(apiClient, 'listMqttMessages').mockImplementation(async (filters) => ({
      items: [
        {
          id: `message-${filters?.page ?? 1}`,
          direction: 'inbound',
          topic: 'vda5050/v3/ResearchBot/RB001/state',
          qos: 0,
          retain: false,
          robotId: 'robot-1',
          messageType: 'state',
          payload: { headerId: 7, battery: 80 },
          schemaValid: false,
          validationErrors: ['timestamp is required'],
          createdAt: '2026-06-29T20:00:00.000Z',
        },
      ],
      page: filters?.page ?? 1,
      pageSize: 20,
      total: 21,
      pages: 2,
    }));
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const router = createRouter({
      routeTree,
      history: createMemoryHistory({ initialEntries: ['/mqtt'] }),
    });
    render(
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>,
    );

    expect(await screen.findByRole('heading', { name: 'MQTT / VDA Logs' })).toBeInTheDocument();
    fireEvent.click(await screen.findByRole('button', { name: 'Inspect' }));
    expect(screen.getByText('timestamp is required')).toBeInTheDocument();
    expect(screen.getByText(/"headerId": 7/)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText('Schema'), { target: { value: 'false' } });
    await waitFor(() =>
      expect(listMessages).toHaveBeenCalledWith(
        expect.objectContaining({ schemaValid: false, page: 1, pageSize: 20 }),
      ),
    );

    await waitFor(() => expect(screen.getByRole('button', { name: 'Next' })).toBeEnabled());
    fireEvent.click(screen.getByRole('button', { name: 'Next' }));
    await waitFor(() =>
      expect(listMessages).toHaveBeenCalledWith(expect.objectContaining({ page: 2 })),
    );
    expect(await screen.findByText(/page 2 of 2/)).toBeInTheDocument();
  });
});

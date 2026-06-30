import '@testing-library/jest-dom/vitest';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import {
  createMemoryHistory,
  createRouter,
  RouterProvider,
} from '@tanstack/react-router';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '../api/client';
import { routeTree } from '../app/router';

class FakeWebSocket {
  addEventListener() {}
  close() {}
}

function renderRoute(path: string) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const router = createRouter({
    routeTree,
    history: createMemoryHistory({ initialEntries: [path] }),
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
}

describe('fleet pages', () => {
  beforeEach(() => {
    vi.stubGlobal('WebSocket', FakeWebSocket);
    vi.stubGlobal('scrollTo', vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('lists API robots and links to their details', async () => {
    vi.spyOn(apiClient, 'listRobots').mockResolvedValue([
      {
        id: 'robot-1',
        manufacturer: 'ResearchBot',
        serialNumber: 'RB001',
        displayName: 'Picker one',
        protocolVersion: '3.0.0',
        lastConnectionState: 'ONLINE',
      },
    ]);

    renderRoute('/robots');

    expect(await screen.findByText('Picker one')).toBeInTheDocument();
    expect(screen.getByText('ResearchBot')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: 'Open' })).toHaveAttribute(
      'href',
      '/robots/robot-1',
    );
  });

  it('shows state and factsheet and publishes cancelOrder after confirmation', async () => {
    vi.spyOn(apiClient, 'getRobot').mockResolvedValue({
      id: 'robot-1',
      manufacturer: 'ResearchBot',
      serialNumber: 'RB001',
      displayName: 'Picker one',
      protocolVersion: '3.0.0',
      lastConnectionState: 'ONLINE',
    });
    vi.spyOn(apiClient, 'getRobotState').mockResolvedValue({
      robotId: 'robot-1',
      batteryCharge: 72,
      operatingMode: 'AUTOMATIC',
      lastNodeId: 'Dock',
      orderId: 'order-1',
      rawPayload: { headerId: 10 },
    });
    vi.spyOn(apiClient, 'getRobotFactsheet').mockResolvedValue({
      typeSpecification: { seriesName: 'ResearchBot' },
    });
    const sendInstantAction = vi.spyOn(apiClient, 'sendInstantAction').mockResolvedValue({
      accepted: true,
      topic: 'vda5050/v3/ResearchBot/RB001/instantActions',
      payload: {},
      errors: [],
    });
    vi.spyOn(window, 'confirm').mockReturnValue(true);

    renderRoute('/robots/robot-1');

    expect(await screen.findByRole('heading', { name: 'Picker one' })).toBeInTheDocument();
    expect(await screen.findByText('72%')).toBeInTheDocument();
    expect(await screen.findByText(/seriesName/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: 'Cancel current order' }));

    await waitFor(() => expect(sendInstantAction).toHaveBeenCalledWith('robot-1', 'cancelOrder'));
    expect(await screen.findByRole('status')).toHaveTextContent('cancelOrder was published');
  });
});

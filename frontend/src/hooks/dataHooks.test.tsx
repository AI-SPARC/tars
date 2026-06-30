import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderHook, waitFor } from '@testing-library/react';
import type { ReactNode } from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { apiClient } from '../api/client';
import { useMaps } from './useMaps';
import { useMissions } from './useMissions';
import { useRobots } from './useRobots';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('fleet query hooks', () => {
  it('loads robots, maps, and missions through React Query', async () => {
    vi.spyOn(apiClient, 'listRobots').mockResolvedValue([
      {
        id: 'robot-1',
        manufacturer: 'ResearchBot',
        serialNumber: 'RB001',
        displayName: null,
        protocolVersion: '3.0.0',
        lastConnectionState: 'ONLINE',
      },
    ]);
    vi.spyOn(apiClient, 'listMaps').mockResolvedValue([
      { id: 'map-1', name: 'Lab', description: null },
    ]);
    vi.spyOn(apiClient, 'listMissions').mockResolvedValue([
      {
        id: 'mission-1',
        mapId: 'map-1',
        assignedRobotId: 'robot-1',
        startNodeKey: 'A',
        goalNodeKey: 'B',
        status: 'assigned',
        priority: 0,
      },
    ]);
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const wrapper = ({ children }: { children: ReactNode }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );

    const robots = renderHook(() => useRobots(), { wrapper });
    const maps = renderHook(() => useMaps(), { wrapper });
    const missions = renderHook(() => useMissions(), { wrapper });

    await waitFor(() => expect(robots.result.current.isSuccess).toBe(true));
    await waitFor(() => expect(maps.result.current.isSuccess).toBe(true));
    await waitFor(() => expect(missions.result.current.isSuccess).toBe(true));
    expect(robots.result.current.data?.[0].serialNumber).toBe('RB001');
    expect(maps.result.current.data?.[0].name).toBe('Lab');
    expect(missions.result.current.data?.[0].status).toBe('assigned');
  });
});

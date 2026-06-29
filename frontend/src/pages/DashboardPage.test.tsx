import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { useMaps } from '../hooks/useMaps';
import { useMissions } from '../hooks/useMissions';
import { useMqttMessages } from '../hooks/useMqttMessages';
import { useRobots } from '../hooks/useRobots';
import { DashboardPage } from './DashboardPage';

vi.mock('../hooks/useMaps');
vi.mock('../hooks/useMissions');
vi.mock('../hooks/useMqttMessages');
vi.mock('../hooks/useRobots');

const successfulQuery = <T,>(data: T) =>
  ({ data, isLoading: false, isError: false, error: null }) as never;

describe('DashboardPage', () => {
  beforeEach(() => {
    vi.mocked(useRobots).mockReturnValue(
      successfulQuery([
        {
          id: 'robot-1',
          manufacturer: 'ResearchBot',
          serialNumber: 'RB001',
          displayName: 'Picker one',
          protocolVersion: '3.0.0',
          lastConnectionState: 'ONLINE',
        },
        {
          id: 'robot-2',
          manufacturer: 'ResearchBot',
          serialNumber: 'RB002',
          displayName: null,
          protocolVersion: '3.0.0',
          lastConnectionState: 'OFFLINE',
        },
      ]),
    );
    vi.mocked(useMissions).mockReturnValue(
      successfulQuery([
        {
          id: 'mission-1',
          mapId: 'map-1',
          assignedRobotId: 'robot-1',
          startNodeKey: 'A',
          goalNodeKey: 'B',
          status: 'sent',
          priority: 0,
        },
        {
          id: 'mission-2',
          mapId: 'map-1',
          assignedRobotId: 'robot-2',
          startNodeKey: 'B',
          goalNodeKey: 'C',
          status: 'completed',
          priority: 0,
        },
      ]),
    );
    vi.mocked(useMaps).mockReturnValue(
      successfulQuery([{ id: 'map-1', name: 'Lab', description: null }]),
    );
    vi.mocked(useMqttMessages)
      .mockReturnValueOnce(
        successfulQuery({
          items: [
            {
              id: 'message-1',
              direction: 'inbound',
              topic: 'vda5050/v3/ResearchBot/RB001/state',
              qos: 0,
              retain: false,
              robotId: 'robot-1',
              messageType: 'state',
              payload: {},
              schemaValid: true,
              validationErrors: [],
              createdAt: '2026-06-29T20:00:00.000Z',
            },
          ],
          page: 1,
          pageSize: 6,
          total: 1,
          pages: 1,
        }),
      )
      .mockReturnValueOnce(
        successfulQuery({ items: [], page: 1, pageSize: 1, total: 3, pages: 3 }),
      );
  });

  it('renders operational metrics and recent fleet activity', () => {
    render(<DashboardPage />);

    expect(screen.getByRole('heading', { name: 'Fleet overview.' })).toBeInTheDocument();
    expect(screen.getByText('1 online', { exact: false })).toBeInTheDocument();
    expect(screen.getByText('Picker one')).toBeInTheDocument();
    expect(screen.getByText('RB002')).toBeInTheDocument();
    expect(screen.getByText('state')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });
});
import '@testing-library/jest-dom/vitest';

import { useQuery } from '@tanstack/react-query';

import { apiClient } from '../api/client';
import { queryKeys } from '../api/queryKeys';

export function useRobots() {
  return useQuery({
    queryKey: queryKeys.robots.all,
    queryFn: apiClient.listRobots,
  });
}

export function useRobotState(robotId: string | undefined) {
  return useQuery({
    queryKey: queryKeys.robots.state(robotId ?? ''),
    queryFn: () => apiClient.getRobotState(robotId as string),
    enabled: Boolean(robotId),
  });
}

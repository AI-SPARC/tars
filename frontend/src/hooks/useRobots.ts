import { useMutation, useQueries, useQuery, useQueryClient } from '@tanstack/react-query';

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

export function useRobot(robotId: string | undefined) {
  return useQuery({
    queryKey: queryKeys.robots.detail(robotId ?? ''),
    queryFn: () => apiClient.getRobot(robotId as string),
    enabled: Boolean(robotId),
  });
}

export function useRobotFactsheet(robotId: string | undefined) {
  return useQuery({
    queryKey: queryKeys.robots.factsheet(robotId ?? ''),
    queryFn: () => apiClient.getRobotFactsheet(robotId as string),
    enabled: Boolean(robotId),
    retry: false,
  });
}

export function useCancelOrder(robotId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => apiClient.sendInstantAction(robotId, 'cancelOrder'),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.robots.state(robotId) });
      void queryClient.invalidateQueries({ queryKey: queryKeys.mqtt.all });
    },
  });
}

export function useRobotStates(robotIds: string[]) {
  return useQueries({
    queries: robotIds.map((robotId) => ({
      queryKey: queryKeys.robots.state(robotId),
      queryFn: () => apiClient.getRobotState(robotId),
      retry: false,
    })),
  });
}

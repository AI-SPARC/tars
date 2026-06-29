import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { apiClient, type MissionInput } from '../api/client';
import { queryKeys } from '../api/queryKeys';

export function useMissions() {
  return useQuery({
    queryKey: queryKeys.missions.all,
    queryFn: apiClient.listMissions,
  });
}

export function useCreateMission() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: MissionInput) => apiClient.createMission(input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.missions.all }),
  });
}

export function useDispatchMission() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (missionId: string) => apiClient.dispatchMission(missionId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.missions.all });
      void queryClient.invalidateQueries({ queryKey: queryKeys.mqtt.all });
    },
  });
}

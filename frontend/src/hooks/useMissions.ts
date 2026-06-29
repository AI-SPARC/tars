import { useQuery } from '@tanstack/react-query';

import { apiClient } from '../api/client';
import { queryKeys } from '../api/queryKeys';

export function useMissions() {
  return useQuery({
    queryKey: queryKeys.missions.all,
    queryFn: apiClient.listMissions,
  });
}

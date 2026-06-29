import { useQuery } from '@tanstack/react-query';

import { apiClient } from '../api/client';
import { queryKeys } from '../api/queryKeys';

export function useMaps() {
  return useQuery({
    queryKey: queryKeys.maps.all,
    queryFn: apiClient.listMaps,
  });
}

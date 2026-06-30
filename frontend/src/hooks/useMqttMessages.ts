import { useQuery } from '@tanstack/react-query';

import { apiClient, type MqttMessageFilters } from '../api/client';
import { queryKeys } from '../api/queryKeys';

export function useMqttMessages(filters: MqttMessageFilters = {}) {
  return useQuery({
    queryKey: queryKeys.mqtt.list(filters),
    queryFn: () => apiClient.listMqttMessages(filters),
  });
}

export const queryKeys = {
  health: ['health'] as const,
  robots: {
    all: ['robots'] as const,
    state: (robotId: string) => ['robots', robotId, 'state'] as const,
  },
  maps: {
    all: ['maps'] as const,
  },
  missions: {
    all: ['missions'] as const,
  },
  mqtt: {
    all: ['mqtt-messages'] as const,
    list: (filters: Record<string, unknown>) => ['mqtt-messages', filters] as const,
  },
};

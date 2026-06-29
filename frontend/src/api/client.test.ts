import { afterEach, describe, expect, it, vi } from 'vitest';

import { ApiError, createApiClient } from './client';

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('API client', () => {
  it('normalizes the base URL and returns typed resources', async () => {
    const robots = [{ id: 'robot-1', manufacturer: 'ResearchBot' }];
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify(robots), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);

    const result = await createApiClient('http://localhost:8000/api/v1/').listRobots();

    expect(result).toEqual(robots);
    expect(fetchMock).toHaveBeenCalledWith('http://localhost:8000/api/v1/robots', {
      headers: { Accept: 'application/json' },
    });
  });

  it('serializes MQTT log filters using the backend contract', async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ items: [], page: 2, pageSize: 25, total: 0, pages: 0 }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);

    await createApiClient('/api/v1').listMqttMessages({
      direction: 'inbound',
      messageType: 'state',
      schemaValid: false,
      page: 2,
      pageSize: 25,
    });

    expect(fetchMock.mock.calls[0][0]).toBe(
      '/api/v1/mqtt/messages?direction=inbound&messageType=state&schemaValid=false&page=2&pageSize=25',
    );
  });

  it('exposes status and FastAPI error details', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: ['Mission has no map'] }), {
          status: 400,
          headers: { 'content-type': 'application/json' },
        }),
      ),
    );

    const request = createApiClient('/api/v1').listMissions();

    await expect(request).rejects.toEqual(
      expect.objectContaining<ApiError>({
        name: 'ApiError',
        message: 'Mission has no map',
        status: 400,
        details: { detail: ['Mission has no map'] },
      }),
    );
  });
});

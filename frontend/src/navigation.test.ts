import { describe, expect, it } from 'vitest';

import { getNavigationItems } from './navigation';

describe('getNavigationItems', () => {
  it('contains the MVP fleet manager sections in operator order', () => {
    expect(getNavigationItems().map((item) => item.label)).toEqual([
      'Dashboard',
      'Fleet / Robots',
      'Map & Routes',
      'Missions',
      'Traffic',
      'MQTT / VDA Logs',
      'Settings',
    ]);
  });
});

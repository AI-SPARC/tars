import { describe, expect, it } from 'vitest';

import { getBrandAttribution, getNavigationItems } from './navigation';

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

describe('getBrandAttribution', () => {
  it('exposes the AI-SPARC developed-by attribution for the sidebar', () => {
    expect(getBrandAttribution()).toEqual({
      label: 'Developed by',
      group: 'AI-SPARC',
      logoAlt: 'AI-SPARC logo',
    });
  });
});

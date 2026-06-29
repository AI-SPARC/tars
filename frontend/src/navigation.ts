export type NavigationItem = {
  label: string;
  path: '/' | '/robots' | '/map' | '/missions' | '/traffic' | '/mqtt' | '/settings';
};

export type BrandAttribution = {
  label: string;
  group: string;
  logoAlt: string;
};

export function getNavigationItems(): NavigationItem[] {
  return [
    { label: 'Dashboard', path: '/' },
    { label: 'Fleet / Robots', path: '/robots' },
    { label: 'Map & Routes', path: '/map' },
    { label: 'Missions', path: '/missions' },
    { label: 'Traffic', path: '/traffic' },
    { label: 'MQTT / VDA Logs', path: '/mqtt' },
    { label: 'Settings', path: '/settings' },
  ];
}

export function getBrandAttribution(): BrandAttribution {
  return {
    label: 'Developed by',
    group: 'AI-SPARC',
    logoAlt: 'AI-SPARC logo',
  };
}

export type NavigationItem = {
  label: string;
  path: string;
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

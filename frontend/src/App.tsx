import { Activity, Map, RadioTower, Route, Settings, TrafficCone, Truck } from 'lucide-react';
import { Link, Outlet, useRouterState } from '@tanstack/react-router';

import aiSparcLogo from './assets/ai-sparc-logo.png';
import { Button } from './components/ui/button';
import { Card, CardContent } from './components/ui/card';
import { useEvents } from './hooks/useEvents';
import { getBrandAttribution, getNavigationItems } from './navigation';
import './styles.css';

const icons = [Activity, Truck, Map, Route, TrafficCone, RadioTower, Settings];

export function App() {
  useEvents();
  const items = getNavigationItems();
  const attribution = getBrandAttribution();
  const pathname = useRouterState({ select: (state) => state.location.pathname });

  return (
    <main className="grid min-h-screen min-w-[1024px] grid-cols-[292px_minmax(0,1fr)] bg-background text-foreground [background-image:radial-gradient(circle_at_80%_10%,rgba(0,0,0,0.035),transparent_28rem)]">
      <aside className="flex min-h-screen flex-col justify-between border-r bg-card p-6">
        <div className="grid gap-9">
          <div className="flex items-center gap-3">
            <span className="grid size-10 place-items-center rounded-xl border border-primary bg-primary font-extrabold tracking-[-0.04em] text-primary-foreground">
              T
            </span>
            <div>
              <strong className="block text-[0.96rem] tracking-[-0.02em]">TARS</strong>
              <small className="block text-muted-foreground">VDA 5050 v3.0.0</small>
            </div>
          </div>

          <nav aria-label="Primary navigation" className="grid gap-1.5">
            {items.map((item, index) => {
              const Icon = icons[index];
              return (
                <Button
                  asChild
                  className="h-10 justify-start gap-2 px-3 font-normal"
                  key={item.path}
                  variant={
                    pathname === item.path || (item.path !== '/' && pathname.startsWith(item.path))
                      ? 'outline'
                      : 'ghost'
                  }
                >
                  <Link to={item.path}>
                    <Icon size={17} strokeWidth={1.8} />
                    {item.label}
                  </Link>
                </Button>
              );
            })}
          </nav>
        </div>

        <section aria-label={attribution.label} className="grid gap-3 pt-6">
          <span className="text-[0.68rem] font-bold uppercase tracking-[0.16em] text-muted-foreground">
            {attribution.label}
          </span>
          <Card className="overflow-hidden rounded-2xl shadow-none">
            <CardContent className="p-3">
              <img
                alt={attribution.logoAlt}
                className="h-auto w-full grayscale contrast-125"
                src={aiSparcLogo}
              />
            </CardContent>
          </Card>
        </section>
      </aside>

      <section className="min-w-0 px-10 py-7 pb-10">
        <header className="mb-10 flex min-h-12 items-center justify-between text-sm text-muted-foreground">
          <span>Open-source fleet control</span>
          <strong className="font-medium text-foreground">Topic root: vda5050/v3</strong>
        </header>

        <Outlet />
      </section>
    </main>
  );
}

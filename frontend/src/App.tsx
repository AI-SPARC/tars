import { Activity, Map, RadioTower, Route, Settings, TrafficCone, Truck } from 'lucide-react';

import aiSparcLogo from './assets/ai-sparc-logo.png';
import { Badge } from './components/ui/badge';
import { Button } from './components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { useEvents } from './hooks/useEvents';
import { getBrandAttribution, getNavigationItems } from './navigation';
import './styles.css';

const icons = [Activity, Truck, Map, Route, TrafficCone, RadioTower, Settings];

const featureCards = [
  {
    index: '01',
    title: 'Fleet overview',
    description: 'Online/offline robots, state snapshots, and active VDA errors.',
  },
  {
    index: '02',
    title: 'Mission management',
    description: 'Build, validate, and dispatch VDA-compliant orders.',
  },
  {
    index: '03',
    title: 'MQTT observability',
    description: 'Inspect inbound and outbound protocol messages.',
  },
];

export function App() {
  useEvents();
  const items = getNavigationItems();
  const attribution = getBrandAttribution();

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
                  variant={index === 0 ? 'outline' : 'ghost'}
                >
                  <a href={item.path}>
                    <Icon size={17} strokeWidth={1.8} />
                    {item.label}
                  </a>
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
        <header className="mb-14 flex min-h-12 items-center justify-between text-sm text-muted-foreground">
          <span>Open-source fleet control</span>
          <strong className="font-medium text-foreground">Topic root: vda5050/v3</strong>
        </header>

        <section className="grid grid-cols-[minmax(0,1fr)_268px] items-stretch gap-8">
          <div>
            <Badge className="mb-5 rounded-md px-0 text-[0.72rem] uppercase tracking-[0.18em]" variant="outline">
              Minimal research platform
            </Badge>
            <h1 className="m-0 max-w-[980px] text-[clamp(3.4rem,6.4vw,7.4rem)] leading-[0.88] tracking-[-0.08em] text-foreground">
              Fleet manager for VDA 5050 mobile robots.
            </h1>
            <p className="mt-6 max-w-[680px] text-[1.08rem] leading-[1.65] text-neutral-700">
              A clean Dockerized foundation for missions, graph maps, MQTT telemetry, schema
              validation, and reproducible simulation experiments.
            </p>
          </div>

          <Card className="min-h-[220px] rounded-2xl bg-card/70 shadow-none">
            <CardHeader className="h-full justify-between">
              <CardDescription className="text-[0.72rem] font-bold uppercase tracking-[0.14em]">
                Protocol
              </CardDescription>
              <div>
                <CardTitle className="text-2xl tracking-[-0.04em]">VDA 5050 v3</CardTitle>
                <CardDescription className="mt-3">Validated with official JSON Schemas</CardDescription>
              </div>
            </CardHeader>
          </Card>
        </section>

        <section className="mt-10 grid grid-cols-3 gap-3.5">
          {featureCards.map((card) => (
            <Card className="min-h-[172px] rounded-2xl bg-card/70 shadow-none" key={card.index}>
              <CardHeader>
                <CardDescription className="text-[0.72rem] font-bold uppercase tracking-[0.14em]">
                  {card.index}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <CardTitle className="mb-2 text-base tracking-[-0.03em]">{card.title}</CardTitle>
                <CardDescription className="leading-6">{card.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </section>
      </section>
    </main>
  );
}

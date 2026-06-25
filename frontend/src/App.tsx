import { Activity, Map, RadioTower, Route, Settings, TrafficCone, Truck } from 'lucide-react';

import aiSparcLogo from './assets/ai-sparc-logo.png';
import { getBrandAttribution, getNavigationItems } from './navigation';
import './styles.css';

const icons = [Activity, Truck, Map, Route, TrafficCone, RadioTower, Settings];

export function App() {
  const items = getNavigationItems();
  const attribution = getBrandAttribution();

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="brand">
            <span className="brand-mark">T</span>
            <div>
              <strong>TARS</strong>
              <small>VDA 5050 v3.0.0</small>
            </div>
          </div>
          <nav aria-label="Primary navigation">
            {items.map((item, index) => {
              const Icon = icons[index];
              return (
                <a href={item.path} key={item.path}>
                  <Icon size={17} strokeWidth={1.8} />
                  {item.label}
                </a>
              );
            })}
          </nav>
        </div>

        <section className="developed-by" aria-label={attribution.label}>
          <span>{attribution.label}</span>
          <img src={aiSparcLogo} alt={attribution.logoAlt} />
        </section>
      </aside>

      <section className="content">
        <header className="topbar">
          <span>Open-source fleet control</span>
          <strong>Topic root: vda5050/v3</strong>
        </header>

        <section className="hero">
          <div>
            <p className="eyebrow">Minimal research platform</p>
            <h1>Fleet manager for VDA 5050 mobile robots.</h1>
            <p>
              A clean Dockerized foundation for missions, graph maps, MQTT telemetry, schema
              validation, and reproducible simulation experiments.
            </p>
          </div>
          <div className="status-card">
            <span>Protocol</span>
            <strong>VDA 5050 v3</strong>
            <small>Validated with official JSON Schemas</small>
          </div>
        </section>

        <section className="cards">
          <article>
            <span>01</span>
            <strong>Fleet overview</strong>
            <p>Online/offline robots, state snapshots, and active errors.</p>
          </article>
          <article>
            <span>02</span>
            <strong>Mission management</strong>
            <p>Build, validate, and dispatch VDA-compliant orders.</p>
          </article>
          <article>
            <span>03</span>
            <strong>MQTT observability</strong>
            <p>Inspect inbound and outbound protocol messages.</p>
          </article>
        </section>
      </section>
    </main>
  );
}

import { Activity, Map, RadioTower, Route, Settings, TrafficCone, Truck } from 'lucide-react';

import { getNavigationItems } from './navigation';
import './styles.css';

const icons = [Activity, Truck, Map, Route, TrafficCone, RadioTower, Settings];

export function App() {
  const items = getNavigationItems();

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">T</span>
          <div>
            <strong>TARS</strong>
            <small>VDA 5050 v3.0.0</small>
          </div>
        </div>
        <nav>
          {items.map((item, index) => {
            const Icon = icons[index];
            return (
              <a href={item.path} key={item.path}>
                <Icon size={18} />
                {item.label}
              </a>
            );
          })}
        </nav>
      </aside>
      <section className="content">
        <header className="hero">
          <div>
            <p className="eyebrow">Open-source fleet control</p>
            <h1>Research fleet manager for VDA 5050 mobile robots</h1>
            <p>
              Dockerized FastAPI + React foundation for missions, map graphs, MQTT telemetry,
              VDA schema validation and future simulation experiments.
            </p>
          </div>
          <div className="status-card">
            <span>Protocol</span>
            <strong>VDA 5050 v3</strong>
            <small>Topic root: vda5050/v3</small>
          </div>
        </header>
        <section className="cards">
          <article><strong>Fleet overview</strong><span>Online/offline robots and state snapshots.</span></article>
          <article><strong>Mission management</strong><span>Build and dispatch VDA orders.</span></article>
          <article><strong>MQTT observability</strong><span>Inspect inbound/outbound protocol logs.</span></article>
        </section>
      </section>
    </main>
  );
}

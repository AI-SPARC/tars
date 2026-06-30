import { useState } from 'react';

import type { MqttMessage, MqttMessageFilters } from '../api/client';
import { MqttMessageTable } from '../components/mqtt/MqttMessageTable';
import { PayloadViewer } from '../components/mqtt/PayloadViewer';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { useMqttMessages } from '../hooks/useMqttMessages';
import { useRobots } from '../hooks/useRobots';

const messageTypes = ['connection', 'state', 'factsheet', 'visualization', 'order', 'instantActions', 'zoneSet', 'responses'];

export function MqttLogsPage() {
  const robots = useRobots();
  const [filters, setFilters] = useState<MqttMessageFilters>({ page: 1, pageSize: 20 });
  const messages = useMqttMessages(filters);
  const [selected, setSelected] = useState<MqttMessage>();

  const selectedMessage = messages.data?.items.some((message) => message.id === selected?.id)
    ? selected
    : undefined;

  const updateFilter = (key: keyof MqttMessageFilters, value: string) => {
    setFilters((current) => ({
      ...current,
      [key]: value === '' ? undefined : key === 'schemaValid' ? value === 'true' : value,
      page: 1,
    }));
  };
  const page = filters.page ?? 1;

  return (
    <div className="grid gap-7">
      <header>
        <Badge className="mb-4 uppercase tracking-[0.14em]" variant="outline">Protocol observability</Badge>
        <h1 className="m-0 text-5xl tracking-[-0.06em]">MQTT / VDA Logs</h1>
        <p className="mb-0 mt-3 text-muted-foreground">Inspect persisted inbound and outbound protocol traffic and schema failures.</p>
      </header>
      <Card className="rounded-2xl bg-card/80 shadow-none">
        <CardContent className="grid grid-cols-4 gap-3 pt-6">
          <FilterSelect label="Direction" onChange={(value) => updateFilter('direction', value)} options={['inbound', 'outbound']} />
          <FilterSelect label="Message type" onChange={(value) => updateFilter('messageType', value)} options={messageTypes} />
          <FilterSelect label="Robot" onChange={(value) => updateFilter('robotId', value)} options={(robots.data ?? []).map((robot) => ({ label: robot.displayName || robot.serialNumber, value: robot.id }))} />
          <FilterSelect label="Schema" onChange={(value) => updateFilter('schemaValid', value)} options={[{ label: 'Valid', value: 'true' }, { label: 'Invalid', value: 'false' }]} />
        </CardContent>
      </Card>

      {messages.isError && <div className="rounded-xl border bg-card p-3 text-sm" role="alert">{messages.error.message}</div>}
      <section className="grid grid-cols-[minmax(0,1fr)_380px] items-start gap-4">
        <div className="grid gap-3">
          {messages.isLoading ? <div aria-label="Loading MQTT messages" className="h-64 animate-pulse rounded-xl border bg-card" /> : <MqttMessageTable messages={messages.data?.items ?? []} onSelect={setSelected} selectedId={selectedMessage?.id} />}
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{messages.data?.total ?? 0} messages · page {page} of {Math.max(messages.data?.pages ?? 0, 1)}</span>
            <div className="flex gap-2">
              <Button disabled={page <= 1} onClick={() => setFilters((current) => ({ ...current, page: page - 1 }))} size="sm" variant="outline">Previous</Button>
              <Button disabled={page >= (messages.data?.pages ?? 0)} onClick={() => setFilters((current) => ({ ...current, page: page + 1 }))} size="sm" variant="outline">Next</Button>
            </div>
          </div>
        </div>
        <PayloadViewer message={selectedMessage} />
      </section>
    </div>
  );
}

type FilterOption = string | { label: string; value: string };

function FilterSelect({ label, options, onChange }: { label: string; options: FilterOption[]; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-1 text-xs font-medium">
      {label}
      <select className="h-9 min-w-0 rounded-md border bg-background px-2" onChange={(event) => onChange(event.target.value)}>
        <option value="">All</option>
        {options.map((option) => {
          const value = typeof option === 'string' ? option : option.value;
          const optionLabel = typeof option === 'string' ? option : option.label;
          return <option key={value} value={value}>{optionLabel}</option>;
        })}
      </select>
    </label>
  );
}

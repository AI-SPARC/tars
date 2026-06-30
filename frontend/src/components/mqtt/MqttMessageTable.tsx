import type { MqttMessage } from '../../api/client';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

export function MqttMessageTable({
  messages,
  selectedId,
  onSelect,
}: {
  messages: MqttMessage[];
  selectedId?: string;
  onSelect: (message: MqttMessage) => void;
}) {
  if (messages.length === 0) {
    return (
      <div className="grid h-64 place-items-center rounded-xl border border-dashed text-sm text-muted-foreground">
        No MQTT messages match the current filters.
      </div>
    );
  }

  return (
    <div className="overflow-auto rounded-xl border">
      <table className="w-full min-w-[760px] border-collapse text-left text-sm">
        <thead className="border-b bg-muted/60 text-[0.67rem] uppercase tracking-[0.12em] text-muted-foreground">
          <tr>
            <th className="px-4 py-3">Time</th>
            <th className="px-4 py-3">Direction</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3">Topic</th>
            <th className="px-4 py-3">Schema</th>
            <th className="px-4 py-3 text-right">Payload</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((message) => (
            <tr className={selectedId === message.id ? 'border-b bg-muted/70' : 'border-b last:border-b-0'} key={message.id}>
              <td className="whitespace-nowrap px-4 py-3 text-xs text-muted-foreground">
                <time dateTime={message.createdAt}>{formatTimestamp(message.createdAt)}</time>
              </td>
              <td className="px-4 py-3"><Badge variant="outline">{message.direction}</Badge></td>
              <td className="px-4 py-3 font-semibold">{message.messageType}</td>
              <td className="max-w-80 truncate px-4 py-3 font-mono text-xs" title={message.topic}>{message.topic}</td>
              <td className="px-4 py-3"><Badge variant={message.schemaValid ? 'default' : 'outline'}>{message.schemaValid ? 'valid' : 'invalid'}</Badge></td>
              <td className="px-4 py-3 text-right"><Button onClick={() => onSelect(message)} size="sm" variant="ghost">Inspect</Button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatTimestamp(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(undefined, {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date);
}

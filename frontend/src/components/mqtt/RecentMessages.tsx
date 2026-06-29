import type { MqttMessage } from '../../api/client';
import { Badge } from '../ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export function RecentMessages({ messages }: { messages: MqttMessage[] }) {
  return (
    <Card className="min-h-[320px] rounded-2xl bg-card/80 shadow-none">
      <CardHeader className="flex-row items-start justify-between space-y-0">
        <div>
          <CardTitle className="text-lg tracking-[-0.03em]">Protocol activity</CardTitle>
          <CardDescription className="mt-1">Latest inbound and outbound MQTT messages</CardDescription>
        </div>
        <a className="text-xs font-semibold underline-offset-4 hover:underline" href="/mqtt">
          View logs
        </a>
      </CardHeader>
      <CardContent>
        {messages.length === 0 ? (
          <div className="grid min-h-48 place-items-center rounded-xl border border-dashed text-sm text-muted-foreground">
            No protocol messages recorded yet.
          </div>
        ) : (
          <ul className="m-0 grid list-none gap-1 p-0">
            {messages.slice(0, 6).map((message) => (
              <li
                className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 border-b py-3 last:border-b-0"
                key={message.id}
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <strong className="text-sm font-medium">{message.messageType}</strong>
                    {!message.schemaValid && <Badge variant="outline">invalid</Badge>}
                  </div>
                  <span className="block truncate text-xs text-muted-foreground">
                    {message.topic}
                  </span>
                </div>
                <div className="text-right text-xs text-muted-foreground">
                  <span className="block uppercase">{message.direction}</span>
                  <time dateTime={message.createdAt}>{formatTime(message.createdAt)}</time>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

function formatTime(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';
  return new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(date);
}

import type { MqttMessage } from '../../api/client';
import { Badge } from '../ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export function PayloadViewer({ message }: { message: MqttMessage | undefined }) {
  return (
    <Card className="sticky top-6 rounded-2xl bg-card/90 shadow-none">
      <CardHeader>
        <CardTitle className="text-lg">Payload inspector</CardTitle>
        <CardDescription>
          {message ? message.topic : 'Select a message from the table.'}
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        {!message ? (
          <div className="grid h-72 place-items-center rounded-xl border border-dashed text-sm text-muted-foreground">
            No message selected.
          </div>
        ) : (
          <>
            <dl className="grid grid-cols-2 gap-2 text-xs">
              <Metadata label="Direction" value={message.direction} />
              <Metadata label="Message type" value={message.messageType} />
              <Metadata label="QoS" value={String(message.qos)} />
              <Metadata label="Retained" value={message.retain ? 'yes' : 'no'} />
            </dl>
            <Badge className="w-fit" variant={message.schemaValid ? 'default' : 'outline'}>
              Schema {message.schemaValid ? 'valid' : 'invalid'}
            </Badge>
            {message.validationErrors.length > 0 && (
              <div className="rounded-xl border p-3">
                <strong className="text-xs uppercase tracking-[0.12em]">Validation errors</strong>
                <ul className="mb-0 mt-2 pl-5 text-xs leading-5">
                  {message.validationErrors.map((error) => <li key={error}>{error}</li>)}
                </ul>
              </div>
            )}
            <pre className="m-0 max-h-[520px] overflow-auto rounded-xl bg-neutral-950 p-4 text-xs leading-5 text-neutral-100">
              {JSON.stringify(message.payload, null, 2)}
            </pre>
          </>
        )}
      </CardContent>
    </Card>
  );
}

function Metadata({ label, value }: { label: string; value: string }) {
  return <div className="rounded-lg border bg-background p-2"><dt className="text-muted-foreground">{label}</dt><dd className="m-0 mt-1 font-semibold">{value}</dd></div>;
}

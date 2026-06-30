import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export function OrderPreview({ payload, topic }: { payload: Record<string, unknown>; topic: string }) {
  return (
    <Card className="rounded-2xl bg-card/80 shadow-none">
      <CardHeader>
        <CardTitle className="text-lg">VDA 5050 order</CardTitle>
        <CardDescription className="break-all font-mono text-xs">{topic}</CardDescription>
      </CardHeader>
      <CardContent>
        <pre className="m-0 max-h-[460px] overflow-auto rounded-xl bg-neutral-950 p-4 text-xs leading-5 text-neutral-100">
          {JSON.stringify(payload, null, 2)}
        </pre>
      </CardContent>
    </Card>
  );
}

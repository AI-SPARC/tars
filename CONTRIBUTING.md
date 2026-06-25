# Contributing

TARS is research-oriented and follows test-driven development for application behavior.

## Local checks

```bash
cd backend
uv run pytest -q
uv run ruff check .

cd ../frontend
npm test -- --run
npm run build
```

## VDA 5050 compliance

When adding protocol behavior, update `docs/vda5050-compliance.md` and add tests using the official schemas under `backend/app/vda5050/schemas/v3_0_0/`.

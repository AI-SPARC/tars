FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN uv sync --no-dev

CMD ["uv", "run", "tars-robot-sim", "--mqtt-host", "mosquitto", "--serial-number", "RB-SIM-001"]

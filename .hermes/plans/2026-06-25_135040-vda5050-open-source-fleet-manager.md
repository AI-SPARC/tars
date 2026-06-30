# VDA-5050 Open-Source Fleet Manager Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

> **Atualização 2026-06-25:** plano ajustado para **VDA 5050 v3.0.0** após envio do PDF `VDA5050-V3.0.0-2025-03.pdf`.

**Goal:** Construir do zero um fleet manager web open-source para pesquisa, compatível inicialmente com VDA 5050 v3.0.0, sem login, com Docker Compose completo, UI inspirada nas capacidades do Meili Robots e base pronta para um client/simulador de testes futuro.

**Architecture:** Aplicação monorepo com backend FastAPI assíncrono, banco PostgreSQL, broker MQTT Mosquitto, frontend React/TypeScript e comunicação em tempo real via WebSocket/SSE. O backend será o `fleet control`: valida mensagens VDA 5050 contra JSON Schemas oficiais, publica `order`/`instantActions`/`zoneSet`/`responses`, consome `state`/`connection`/`factsheet`/`visualization`, persiste telemetria e expõe APIs para mapas, robôs, missões, tráfego e observabilidade.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2, jsonschema, aiomqtt/paho-mqtt, PostgreSQL, Mosquitto, pytest, Ruff, mypy; React 19 + Vite + TypeScript, TanStack Query/Router, Zustand, Tailwind + shadcn/ui, React Flow ou Konva para editor/visualizador de mapa, Vitest/Playwright; Docker Compose para `backend`, `frontend`, `postgres`, `mosquitto`.

---

## 1. Evidências e decisões iniciais

### 1.1 VDA 5050

Fontes consultadas:

- PDF local: `C:\Users\geova\Downloads\VDA5050-V3.0.0-2025-03.pdf`.
- GitHub: `https://github.com/VDA5050/VDA5050`.
- Tag/release-alvo do repositório: `3.0.0`.

Decisão:

- **Target inicial: VDA 5050 v3.0.0**, porque o PDF atualizado enviado é `Version 3.0.0, March 2026` e o GitHub `main` também publica a versão `3.0.0`.
- A implementação deve pinzar schemas no tag `3.0.0` para reprodutibilidade:
  - `https://raw.githubusercontent.com/VDA5050/VDA5050/3.0.0/json_schemas/order.schema`
  - `.../instantActions.schema`
  - `.../state.schema`
  - `.../connection.schema`
  - `.../factsheet.schema`
  - `.../visualization.schema`
  - `.../zoneSet.schema`
  - `.../responses.schema`
- Guardar os schemas versionados no repo para builds reprodutíveis, sem depender de rede em runtime.

Pontos normativos relevantes do PDF v3.0.0:

- Transporte: MQTT com payload JSON.
- MQTT mínimo: 3.1.1.
- QoS:
  - `order`, `instantActions`, `state`, `factsheet`, `zoneSet`, `responses`, `visualization`: QoS 0.
  - `connection`: QoS 1.
- Estrutura de tópico local sugerida:
  - `interfaceName/majorVersion/manufacturer/serialNumber/topic`
  - Exemplo: `vda5050/v3/KIT/0001/order`.
- Caracteres que não devem aparecer em campos de tópico/identidade: `/`, wildcards `+` e `#`, e `$`.
- Tópicos VDA 5050 v3.0.0:
  - `order`: fleet control -> mobile robot, obrigatório.
  - `instantActions`: fleet control -> mobile robot, obrigatório.
  - `state`: mobile robot -> fleet control, obrigatório.
  - `connection`: broker/mobile robot -> fleet control, obrigatório.
  - `factsheet`: mobile robot -> fleet control, obrigatório.
  - `visualization`: mobile robot -> sistemas de visualização, opcional; inclui posição e planned path de alta frequência.
  - `zoneSet`: fleet control -> mobile robot, opcional.
  - `responses`: fleet control -> mobile robot, opcional; respostas do fleet control para requests vindos no `state`.
- Header comum não encapsulado como objeto:
  - `headerId`, `timestamp`, `version`, `manufacturer`, `serialNumber`.
- Ordem VDA:
  - Grafo de `nodes[]` e `edges[]`.
  - Ordem válida: pelo menos 1 node; `len(edges) == len(nodes) - 1`.
  - `sequenceId` é compartilhado entre nodes e edges, contínuo: primeiro node `0`, primeira edge `1`, segundo node `2`, etc.
  - A primeira node (`sequenceId=0`) deve ser trivialmente alcançável, sempre `released=true`, e não deve ser reportada em `nodeStates`.
  - `released=true` compõe a base; `released=false` compõe o horizon.
  - A base não deve ser alterada; updates usam `orderId` igual e `orderUpdateId` incrementado.
  - O primeiro node de um update deve costurar no último node da base anterior; v3.0.0 também documenta update com stitching node adicional para executar novas actions no decision point.
- Cancelamento via instant action `cancelOrder`.
- V3.0.0 expande o modelo com zonas (`zoneSet`), request/response mechanism, compartilhamento de planned paths para mobile robots livremente navegantes, e linguagem atualizada de **fleet control** / **mobile robot** em vez de **master control** / **AGV**.
- Funções esperadas do fleet control: alocação de ordens, cálculo de rota, controle de tráfego, deadlock/blockage handling, energia/carregamento, posições de espera/buffer, mudanças temporárias do ambiente, comunicação com periféricos e detecção de erros de comunicação.

### 1.2 Inspiração Meili Robots

Funcionalidades/telas extraídas como referência pública do site:

- Fleet overview.
- Mission management.
- Traffic control.
- Route planning.
- IoT device integrations.
- Custom stations & paths.
- Plug & play vehicle management.
- Fleet charge management.
- Multifloor capabilities.
- Custom actions.
- Site settings.
- RTLS/connectivity.
- Advanced zones.
- Emergency stop/safety policies.
- Audit logs/analytics/export.

Decisão de escopo para pesquisa/open-source:

- **Sem login, sem billing, sem 2FA/SMS/permissões** no MVP.
- Priorizar interoperabilidade, simulação/testabilidade, observabilidade e aderência VDA 5050.

### 1.3 Estado atual do repo

Repo atual: `C:\Users\geova\repos\research\tars`.

Há backend FastAPI parcial em `backend/`, com mobile robot CRUD básico, SQLAlchemy, Alembic e testes. O usuário autorizou descartar tudo. Plano assume **reestruturação do zero**, preservando apenas o histórico Git.

---

## 2. Escopo por versões

### MVP v0.1 — Fleet manager VDA observável e operável

Objetivo: subir via Docker, cadastrar/descobrir robôs, receber telemetria VDA, mostrar frota no mapa, criar ordem simples e publicar via MQTT.

Inclui:

1. Docker Compose completo.
2. Backend FastAPI com healthcheck, OpenAPI e WebSocket/SSE.
3. PostgreSQL + Alembic.
4. Mosquitto configurado.
5. Schemas VDA 5050 v3.0.0 versionados no repo.
6. Validação JSON Schema para tópicos VDA.
7. MQTT adapter:
   - subscribe `vda5050/v3/+/+/state`
   - subscribe `vda5050/v3/+/+/connection`
   - subscribe `vda5050/v3/+/+/factsheet`
   - subscribe `vda5050/v3/+/+/visualization`
   - publish `order`
   - publish `instantActions`
   - publish `zoneSet` opcional
   - publish `responses` opcional
8. Cadastro/descoberta de veículos por `manufacturer + serialNumber`.
9. Persistência de último estado e histórico resumido.
10. Editor simples de mapa grafo: nodes/edges/stations.
11. Criação de missão de ponto A -> B.
12. Planejamento inicial com caminho mais curto em grafo dirigido/ponderado.
13. Geração de `order` VDA com nodes/edges e `sequenceId` correto.
14. Dashboard web:
    - visão geral da frota;
    - mapa com posições;
    - lista de missões;
    - detalhes do robô;
    - logs MQTT/VDA;
    - envio de instant actions básicas.
15. Testes unitários e integração com broker MQTT em container.
16. Documentação para rodar e desenvolver.

### v0.2 — Pesquisa em alocação, tráfego e simulação

Inclui:

1. Client/simulador VDA 5050 separado, dentro de `simulator/` ou `clients/python-simulator/`.
2. Alocação de tarefas multi-robô.
3. Reserva de trechos/nodes para traffic control.
4. Zonas, bloqueios temporários e waiting positions.
5. Estratégias de roteamento plugáveis.
6. Métricas de pesquisa: tempo de missão, ociosidade, distância, congestionamento, carga de bateria.
7. Export CSV/JSON.

### v0.3 — Extensibilidade e interoperabilidade

Inclui:

1. Suporte opcional a VDA 5050 v2.1.0 lado a lado, se houver necessidade de compatibilidade legada.
2. Plugins de algoritmo.
3. Integração ROS/ROS2 via client separado.
4. Import/export de mapas.
5. Replays e cenários reproduzíveis.

### Pós-v1 — Interoperabilidade de mapas e planejamento plugável

Estas melhorias ficam deliberadamente fora do caminho crítico da v1 e devem ser iniciadas após
o fechamento do MVP operacional, dos testes E2E e da matriz de compliance.

#### Mapas fornecidos pelo usuário

1. Definir um formato canônico, versionado e documentado para import/export do grafo completo.
2. Criar API transacional de bulk import com validação, dry-run e relatório de erros por elemento.
3. Suportar inicialmente JSON e CSV; adicionar adaptadores opcionais para GeoJSON e mapas ROS/ROS2.
4. Registrar sistema de coordenadas, unidade, origem, floor e metadados de transformação.
5. Adicionar versionamento de mapas, histórico de alterações, clone e rollback.
6. Permitir atualização e exclusão seguras, verificando missões e reservas que referenciam o mapa.
7. Criar export reproduzível para datasets e experimentos de pesquisa.

#### Algoritmos de planejamento substituíveis

1. Extrair o cálculo de rota de `MapService` para um contrato `RoutePlanner` independente.
2. Criar registry/factory de planejadores selecionáveis por configuração e, opcionalmente, missão.
3. Manter Dijkstra como baseline e adicionar A*, menor tempo, energia e custos multiobjetivo.
4. Definir `PlanningContext` para bloqueios, capacidade, bateria, reservas e restrições do robô.
5. Permitir plugins de algoritmo sem dependência dos modelos SQLAlchemy ou do transporte MQTT.
6. Persistir algoritmo, parâmetros, seed, custo e duração de cada planejamento para reprodução.
7. Criar suíte comum de conformidade para qualquer planner e benchmarks com cenários versionados.
8. Evoluir para planejamento multi-robô, congestionamento e prevenção de deadlock na linha v0.2+.

---

## 3. Estrutura proposta do monorepo

Criar/substituir por:

```text
tars/
  README.md
  LICENSE
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  docker-compose.yml
  docker-compose.dev.yml
  .env.example
  .editorconfig
  .gitignore
  docs/
    architecture.md
    vda5050-compliance.md
    development.md
    mqtt-topics.md
    api.md
    research-use-cases.md
  infra/
    mosquitto/
      mosquitto.conf
      acl.conf
    postgres/
      init.sql
  backend/
    Dockerfile
    pyproject.toml
    alembic.ini
    alembic/
      env.py
      versions/
    app/
      __init__.py
      main.py
      core/
        config.py
        logging.py
        lifespan.py
        errors.py
      db/
        base.py
        session.py
        models/
          robot.py
          robot_state.py
          map.py
          mission.py
          mqtt_message.py
          traffic.py
        repositories/
      vda5050/
        schemas/v3_0_0/
          order.schema.json
          instantActions.schema.json
          state.schema.json
          connection.schema.json
          factsheet.schema.json
          visualization.schema.json
          zoneSet.schema.json
          responses.schema.json
        validator.py
        topics.py
        envelope.py
        order_builder.py
        instant_actions.py
        compliance.py
      mqtt/
        client.py
        router.py
        handlers.py
        publisher.py
      api/
        deps.py
        v1/
          router.py
          health.py
          robots.py
          maps.py
          missions.py
          traffic.py
          mqtt.py
          events.py
      services/
        robot_registry.py
        map_service.py
        route_planner.py
        mission_service.py
        traffic_service.py
        telemetry_service.py
        event_bus.py
      tests/
        unit/
        integration/
  frontend/
    Dockerfile
    package.json
    vite.config.ts
    tsconfig.json
    src/
      main.tsx
      app/
        router.tsx
        queryClient.ts
      api/
        client.ts
        generated.ts
      components/
        layout/
        fleet/
        map/
        missions/
        robots/
        mqtt/
        ui/
      pages/
        DashboardPage.tsx
        MapPage.tsx
        RobotsPage.tsx
        RobotDetailPage.tsx
        MissionsPage.tsx
        MissionBuilderPage.tsx
        TrafficPage.tsx
        MqttLogsPage.tsx
        SettingsPage.tsx
      stores/
      hooks/
      styles/
      tests/
  clients/
    README.md
    python-simulator/        # v0.2, não obrigatório no MVP
```

---

## 4. Modelo de domínio inicial

### 4.1 Entidades principais

Backend models:

- `Robot`
  - `id`
  - `manufacturer`
  - `serial_number`
  - `display_name`
  - `protocol_version`
  - `last_connection_state`
  - `last_seen_at`
  - `factsheet`
  - `capabilities`
  - unique `(manufacturer, serial_number)`

- `RobotStateSnapshot`
  - `id`
  - `robot_id`
  - `header_id`
  - `order_id`
  - `order_update_id`
  - `last_node_id`
  - `last_node_sequence_id`
  - `battery_charge`
  - `operating_mode`
  - `errors`
  - `safety_state`
  - `agv_position`
  - `node_states`
  - `edge_states`
  - `action_states`
  - `raw_payload`
  - `received_at`

- `Map`
  - `id`
  - `name`
  - `description`
  - `coordinate_system`
  - `floor`
  - `metadata`

- `MapNode`
  - `id`
  - `map_id`
  - `node_key`
  - `x`, `y`, `theta`
  - `allowed_deviation_xy`
  - `type`: `station`, `waypoint`, `charger`, `buffer`, `gate`, `elevator`

- `MapEdge`
  - `id`
  - `map_id`
  - `edge_key`
  - `from_node_id`
  - `to_node_id`
  - `distance`
  - `max_speed`
  - `bidirectional`
  - `restrictions`

- `Mission`
  - `id`
  - `mission_code`
  - `status`: `draft`, `queued`, `assigned`, `sent`, `running`, `completed`, `failed`, `cancelled`
  - `assigned_robot_id`
  - `start_node_id`
  - `goal_node_id`
  - `priority`
  - `created_at`, `updated_at`

- `MissionOrder`
  - `id`
  - `mission_id`
  - `robot_id`
  - `order_id`
  - `order_update_id`
  - `payload`
  - `validation_status`
  - `published_at`

- `MqttMessageLog`
  - `id`
  - `direction`: `inbound`/`outbound`
  - `topic`
  - `qos`
  - `robot_id`
  - `message_type`
  - `payload`
  - `schema_valid`
  - `validation_errors`
  - `created_at`

- `TrafficReservation` v0.2-ready
  - `id`
  - `robot_id`
  - `mission_id`
  - `resource_type`: `node`/`edge`/`zone`
  - `resource_id`
  - `status`
  - `reserved_from`, `reserved_until`

### 4.2 Identidade do robô

Usar identidade VDA:

```text
robot_key = manufacturer + ":" + serialNumber
```

O registry cria automaticamente o `Robot` quando recebe `state`, `connection`, `factsheet` ou `visualization` válido de um robô desconhecido.

---

## 5. API inicial

Prefixo: `/api/v1`.

Endpoints:

```text
GET    /health
GET    /vda5050/schemas
POST   /vda5050/validate/{message_type}

GET    /robots
POST   /robots
GET    /robots/{robot_id}
PATCH  /robots/{robot_id}
GET    /robots/{robot_id}/state/latest
GET    /robots/{robot_id}/states
GET    /robots/{robot_id}/factsheet
POST   /robots/{robot_id}/instant-actions

GET    /maps
POST   /maps
GET    /maps/{map_id}
PUT    /maps/{map_id}
DELETE /maps/{map_id}
POST   /maps/{map_id}/nodes
POST   /maps/{map_id}/edges
POST   /maps/{map_id}/route-preview

GET    /missions
POST   /missions
GET    /missions/{mission_id}
POST   /missions/{mission_id}/assign
POST   /missions/{mission_id}/dispatch
POST   /missions/{mission_id}/cancel

GET    /mqtt/messages
WS     /events/ws
```

Eventos em tempo real via WebSocket:

```json
{
  "type": "robot.state.updated",
  "robotId": "...",
  "payload": {}
}
```

Tipos mínimos:

- `robot.discovered`
- `robot.connection.updated`
- `robot.state.updated`
- `robot.visualization.updated`
- `mission.created`
- `mission.assigned`
- `mission.dispatched`
- `mission.status.changed`
- `mqtt.message.received`
- `mqtt.message.published`
- `vda.validation.failed`

---

## 6. Telas do frontend

### 6.1 Layout base

Sidebar:

1. Dashboard
2. Fleet / Robots
3. Map & Routes
4. Missions
5. Traffic
6. MQTT / VDA Logs
7. Settings
8. Documentation

Header:

- status API;
- status broker MQTT;
- quantidade de robôs online/offline;
- versão VDA ativa.

### 6.2 Dashboard

Cards:

- Robots online/offline.
- Missões em fila/em execução/concluídas/falhas.
- Erros VDA ativos.
- Bateria média.
- Últimas mensagens MQTT.

Widgets:

- mapa pequeno com posições;
- tabela de robôs;
- timeline de eventos.

### 6.3 Fleet / Robots

Tabela:

- nome;
- manufacturer;
- serialNumber;
- conexão;
- modo operacional;
- bateria;
- missão atual;
- último estado.

Detalhe do robô:

- estado VDA bruto formatado;
- factsheet;
- action states;
- errors/warnings;
- histórico;
- botão `cancelOrder`;
- botão para instant action customizada.

### 6.4 Map & Routes

Funcionalidades MVP:

- Criar mapa.
- Criar nodes clicando no canvas.
- Criar edges arrastando/conectando nodes.
- Marcar node como station/charger/buffer.
- Mostrar posição dos robôs (`agvPosition` ou último node).
- Preview de rota A -> B.

### 6.5 Missions

Funcionalidades MVP:

- Criar missão escolhendo origem/destino/priority.
- Selecionar robô manualmente no MVP.
- Preview do payload `order` VDA antes de publicar.
- Validar payload contra schema.
- Dispatch via MQTT.
- Acompanhar status.

### 6.6 Traffic

MVP simples:

- Visualizar edges/nodes ocupados/planejados.
- Mostrar conflitos detectados de forma informativa.

v0.2:

- Reserva de trechos.
- Zonas e bloqueios temporários.
- Deadlock detection.

### 6.7 MQTT / VDA Logs

Tabela filtrável:

- horário;
- direção;
- tópico;
- robot;
- schema valid/invalid;
- payload JSON;
- erro de validação.

---

## 7. Plano de implementação por fases

## Phase 0 — Reset controlado e fundação do repo

### Task 0.1: Criar branch e registrar decisão de rewrite

**Objective:** Trabalhar sem destruir histórico e deixar explícito que o código antigo será substituído.

**Files:**
- Modify/Create: `docs/architecture.md`

**Steps:**

1. Criar branch:
   ```bash
   git checkout -b rewrite/vda5050-fleet-manager
   ```
2. Criar `docs/architecture.md` com visão geral e decisão de rewrite.
3. Commit:
   ```bash
   git add docs/architecture.md
   git commit -m "docs: record vda5050 fleet manager rewrite architecture"
   ```

### Task 0.2: Criar estrutura monorepo mínima

**Objective:** Criar diretórios limpos para backend, frontend, infra e docs.

**Files:**
- Create/Replace: estrutura listada na seção 3.

**Steps:**

1. Remover conteúdo antigo de `backend/` ou mover para `legacy/` temporariamente se quiser preservar referência.
2. Criar diretórios vazios com `.gitkeep` onde necessário.
3. Commit:
   ```bash
   git add .
   git commit -m "chore: initialize monorepo structure"
   ```

### Task 0.3: Adicionar documentação inicial

**Objective:** Ter README útil para pesquisadores desde o início.

**Files:**
- Replace: `README.md`
- Create: `docs/development.md`
- Create: `docs/vda5050-compliance.md`
- Create: `docs/mqtt-topics.md`

**Conteúdo mínimo do README:**

- O que é o projeto.
- Escopo VDA 5050 v3.0.0.
- Quickstart Docker.
- Arquitetura resumida.
- Status experimental/research.
- Licença.

**Verification:**

- README deve mencionar explicitamente: FastAPI, React, PostgreSQL, Mosquitto, VDA 5050 v3.0.0.

---

## Phase 1 — Infra Docker e backend base

### Task 1.1: Criar Docker Compose

**Objective:** Subir stack mínima com API, DB, broker e UI.

**Files:**
- Create: `docker-compose.yml`
- Create: `docker-compose.dev.yml`
- Create: `.env.example`
- Create: `infra/mosquitto/mosquitto.conf`
- Create: `infra/mosquitto/acl.conf`

**Services:**

- `postgres:16-alpine`
- `mosquitto:2`
- `backend`
- `frontend`

**Ports:**

- backend: `8000`
- frontend: `5173` dev / `8080` prod
- postgres: `5432`
- mqtt: `1883`
- mqtt websocket opcional: `9001`

**Verification:**

```bash
docker compose config
```

Expected: sem erro.

### Task 1.2: Criar projeto backend com pyproject

**Objective:** Backend instalável e testável.

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/app/main.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/logging.py`
- Create: `backend/app/api/v1/health.py`
- Create: `backend/app/api/v1/router.py`
- Create: `backend/tests/unit/test_health.py`

**Dependencies sugeridas:**

```toml
fastapi
uvicorn[standard]
pydantic
pydantic-settings
sqlalchemy[asyncio]
asyncpg
alembic
aiomqtt
jsonschema
networkx
orjson
structlog
python-dotenv
pytest
pytest-asyncio
httpx
ruff
mypy
```

**Verification:**

```bash
cd backend
uv run pytest -q
uv run ruff check .
```

Expected: testes passam e lint sem erro.

### Task 1.3: Configurar DB async e Alembic

**Objective:** Conectar backend ao PostgreSQL e rodar migrations.

**Files:**
- Create: `backend/app/db/session.py`
- Create: `backend/app/db/base.py`
- Create: `backend/alembic.ini`
- Create: `backend/alembic/env.py`

**Verification:**

```bash
docker compose up -d postgres
cd backend
uv run alembic revision --autogenerate -m "initial empty migration"
uv run alembic upgrade head
```

Expected: migration aplica no banco.

---

## Phase 2 — Núcleo VDA 5050

### Task 2.1: Versionar JSON Schemas VDA 5050 v3.0.0

**Objective:** Validação offline e reprodutível.

**Files:**
- Create: `backend/app/vda5050/schemas/v3_0_0/order.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/instantActions.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/state.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/connection.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/factsheet.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/visualization.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/zoneSet.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/responses.schema.json`
- Create: `backend/app/vda5050/schemas/v3_0_0/README.md`

**Source:** GitHub tag `3.0.0`.

**Verification:**

- Arquivos existem.
- `README.md` contém URLs e commit/tag de origem.

### Task 2.2: Implementar validator VDA

**Objective:** Validar payloads por tipo de mensagem.

**Files:**
- Create: `backend/app/vda5050/validator.py`
- Create: `backend/app/vda5050/compliance.py`
- Create: `backend/tests/unit/vda5050/test_validator.py`

**Behavior:**

- `validate_message(message_type: Literal[...], payload: dict, version="3.0.0") -> ValidationResult`
- Retornar lista de erros amigáveis.
- Não lançar exceção para payload inválido em fluxo normal; retornar resultado inválido.

**Tests:**

- Payload mínimo válido de `connection` passa.
- Payload sem `headerId` falha.
- `message_type` desconhecido falha.

### Task 2.3: Implementar parser de tópicos VDA

**Objective:** Extrair identidade do robô e tipo de mensagem de tópicos MQTT.

**Files:**
- Create: `backend/app/vda5050/topics.py`
- Create: `backend/tests/unit/vda5050/test_topics.py`

**Rules:**

- Parse `vda5050/v3/{manufacturer}/{serialNumber}/{topic}`.
- Rejeitar `/`, wildcards `+`/`#` e `$` em campos de identidade.
- Tópicos aceitos: `order`, `instantActions`, `state`, `connection`, `factsheet`, `visualization`, `zoneSet`, `responses`.

**Tests:**

- `vda5050/v3/KIT/0001/state` -> manufacturer `KIT`, serial `0001`, topic `state`.
- tópico incompleto falha.
- versão incompatível falha com erro claro.

### Task 2.4: Implementar builder de `order`

**Objective:** Gerar payload `order` válido a partir de rota interna.

**Files:**
- Create: `backend/app/vda5050/order_builder.py`
- Create: `backend/tests/unit/vda5050/test_order_builder.py`

**Rules MVP:**

- `headerId` incremental por robô+tópico.
- `timestamp` ISO 8601 UTC.
- `version`: `3.0.0`.
- `orderId`: UUID/string.
- `orderUpdateId`: `0` para nova ordem.
- `sequenceId`: nodes pares `0,2,4...`, edges ímpares `1,3,5...`.
- Todos nodes/edges do MVP podem sair `released=true`.
- `len(edges) == len(nodes)-1`.

**Tests:**

- Rota com 2 nodes gera 2 nodes e 1 edge.
- Rota com 1 node gera edges vazio.
- Payload resultante valida contra `order.schema.json`.

---

## Phase 3 — Persistência e serviços backend

### Task 3.1: Criar models de robôs e snapshots

**Objective:** Persistir registry e último estado.

**Files:**
- Create: `backend/app/db/models/robot.py`
- Create: `backend/app/db/models/robot_state.py`
- Create: migration Alembic
- Create: `backend/tests/integration/db/test_robot_models.py`

**Verification:**

```bash
cd backend
uv run alembic upgrade head
uv run pytest tests/integration/db -q
```

### Task 3.2: Criar RobotRegistryService

**Objective:** Descobrir/upsert robôs por mensagens VDA.

**Files:**
- Create: `backend/app/services/robot_registry.py`
- Create: `backend/tests/unit/services/test_robot_registry.py`

**Behavior:**

- `get_or_create(manufacturer, serial_number)`.
- Atualizar `last_seen_at`.
- Atualizar factsheet.
- Atualizar connection state.

### Task 3.3: Criar MapService e route planner

**Objective:** CRUD de mapas e cálculo de rota.

**Files:**
- Create: `backend/app/db/models/map.py`
- Create: `backend/app/services/map_service.py`
- Create: `backend/app/services/route_planner.py`
- Create: migration Alembic
- Create: tests unitários e integração.

**Implementation:**

- Usar `networkx` para caminho mais curto no MVP.
- Peso padrão: `distance`.
- Validar que nodes pertencem ao mesmo mapa.

### Task 3.4: Criar MissionService

**Objective:** Criar, atribuir, gerar order e despachar missão.

**Files:**
- Create: `backend/app/db/models/mission.py`
- Create: `backend/app/services/mission_service.py`
- Create: tests.

**State machine MVP:**

```text
draft -> queued -> assigned -> sent -> running -> completed
                              -> failed
                              -> cancelled
```

**Rules:**

- Dispatch só se missão `assigned`.
- Gerar `order` e validar antes de publicar.
- Persistir payload em `MissionOrder`.

---

## Phase 4 — MQTT runtime

### Task 4.1: Implementar MQTT client lifecycle

**Objective:** Conectar ao broker no lifespan do FastAPI.

**Files:**
- Create: `backend/app/mqtt/client.py`
- Modify: `backend/app/core/lifespan.py`
- Create: `backend/tests/unit/mqtt/test_client_config.py`

**Behavior:**

- Config por env:
  - `MQTT_HOST`
  - `MQTT_PORT`
  - `MQTT_USERNAME`
  - `MQTT_PASSWORD`
  - `MQTT_INTERFACE_NAME=vda5050`
  - `VDA5050_MAJOR_VERSION=v3`
- Reconexão com backoff.
- Subscribe nos tópicos inbound.

### Task 4.2: Implementar handlers inbound

**Objective:** Processar `state`, `connection`, `factsheet`, `visualization`.

**Files:**
- Create: `backend/app/mqtt/handlers.py`
- Create: `backend/app/mqtt/router.py`
- Create: `backend/app/db/models/mqtt_message.py`
- Create: tests.

**Flow:**

1. Recebe tópico/payload.
2. Parseia tópico.
3. Decodifica JSON.
4. Valida schema.
5. Loga mensagem.
6. Upsert robot.
7. Atualiza snapshot/connection/factsheet.
8. Publica evento WebSocket.

### Task 4.3: Implementar publisher outbound

**Objective:** Publicar `order` e `instantActions` com QoS correto.

**Files:**
- Create: `backend/app/mqtt/publisher.py`
- Create: tests.

**Rules:**

- `order`: QoS 0.
- `instantActions`: QoS 0.
- Logar outbound.
- Validar antes de publicar.

### Task 4.4: Teste de integração com Mosquitto

**Objective:** Provar fluxo MQTT real.

**Files:**
- Create: `backend/tests/integration/mqtt/test_mqtt_flow.py`

**Test:**

1. Subir Mosquitto via Compose ou testcontainer.
2. Publicar `state` fake válido.
3. Verificar robot criado.
4. Criar missão e dispatch.
5. Verificar mensagem publicada em `order`.

---

## Phase 5 — API REST e eventos

### Task 5.1: Implementar APIs de robots

**Files:**
- Create: `backend/app/api/v1/robots.py`
- Tests: `backend/tests/integration/api/test_robots_api.py`

**Endpoints:** conforme seção 5.

### Task 5.2: Implementar APIs de maps

**Files:**
- Create: `backend/app/api/v1/maps.py`
- Tests: `backend/tests/integration/api/test_maps_api.py`

### Task 5.3: Implementar APIs de missions

**Files:**
- Create: `backend/app/api/v1/missions.py`
- Tests: `backend/tests/integration/api/test_missions_api.py`

### Task 5.4: Implementar API de logs MQTT/VDA

**Files:**
- Create: `backend/app/api/v1/mqtt.py`
- Tests: `backend/tests/integration/api/test_mqtt_logs_api.py`

### Task 5.5: Implementar WebSocket de eventos

**Files:**
- Create: `backend/app/services/event_bus.py`
- Create: `backend/app/api/v1/events.py`
- Tests: `backend/tests/integration/api/test_events_ws.py`

---

## Phase 6 — Frontend base

### Task 6.1: Criar projeto React/Vite

**Objective:** UI dev pronta em Docker.

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/app/router.tsx`
- Create: `frontend/src/styles/globals.css`
- Create: `frontend/Dockerfile`

**Dependencies:**

```text
@tanstack/react-query
@tanstack/react-router
zustand
zod
axios ou ky
lucide-react
class-variance-authority
clsx
tailwind-merge
react-hook-form
@hookform/resolvers
reactflow ou react-konva/konva
```

**Verification:**

```bash
cd frontend
npm install
npm run build
npm run test
```

### Task 6.2: Layout e navegação

**Files:**
- Create: `frontend/src/components/layout/AppShell.tsx`
- Create: `frontend/src/components/layout/Sidebar.tsx`
- Create: `frontend/src/components/layout/Header.tsx`
- Create: page placeholders.

**Acceptance:**

- Todas telas navegam sem erro.
- Header mostra status API mockado ou real de `/health`.

### Task 6.3: API client e hooks

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/hooks/useRobots.ts`
- Create: `frontend/src/hooks/useMissions.ts`
- Create: `frontend/src/hooks/useMaps.ts`
- Create: `frontend/src/hooks/useEvents.ts`

**Acceptance:**

- React Query busca `/robots`, `/missions`, `/maps`.
- WebSocket atualiza cache para eventos de estado.

### Task 6.4: Dashboard

**Files:**
- Create: `frontend/src/pages/DashboardPage.tsx`
- Create: components em `frontend/src/components/fleet/`.

**Acceptance:**

- Cards de frota, missões e erros.
- Últimos eventos MQTT/VDA.

### Task 6.5: Fleet / Robot detail

**Files:**
- Create: `frontend/src/pages/RobotsPage.tsx`
- Create: `frontend/src/pages/RobotDetailPage.tsx`
- Create: `frontend/src/components/robots/RobotTable.tsx`
- Create: `frontend/src/components/robots/RobotStatePanel.tsx`

**Acceptance:**

- Lista robôs reais da API.
- Detalhe mostra state/factsheet JSON.
- Botão de `cancelOrder` chama API.

### Task 6.6: Map editor/viewer

**Files:**
- Create: `frontend/src/pages/MapPage.tsx`
- Create: `frontend/src/components/map/MapCanvas.tsx`
- Create: `frontend/src/components/map/NodeEditor.tsx`
- Create: `frontend/src/components/map/EdgeEditor.tsx`

**Acceptance:**

- Criar node.
- Criar edge.
- Salvar mapa.
- Exibir robôs sobre o mapa.

### Task 6.7: Mission builder

**Files:**
- Create: `frontend/src/pages/MissionsPage.tsx`
- Create: `frontend/src/pages/MissionBuilderPage.tsx`
- Create: `frontend/src/components/missions/MissionForm.tsx`
- Create: `frontend/src/components/missions/OrderPreview.tsx`

**Acceptance:**

- Escolher origem/destino/robô.
- Preview de rota.
- Criar missão.
- Dispatch.
- Exibir payload order.

### Task 6.8: MQTT/VDA logs

**Files:**
- Create: `frontend/src/pages/MqttLogsPage.tsx`
- Create: `frontend/src/components/mqtt/MqttMessageTable.tsx`
- Create: `frontend/src/components/mqtt/PayloadViewer.tsx`

**Acceptance:**

- Filtros por direção, tipo, robot e validade.
- JSON pretty print.

---

## Phase 7 — Compliance, docs e QA

### Task 7.1: Criar matriz de compliance VDA 5050

**Files:**
- Update: `docs/vda5050-compliance.md`

**Tabela:**

```text
Requirement | Source PDF section | Status | Implementation | Tests
```

Cobrir inicialmente:

- Topic structure.
- QoS.
- Header fields.
- Schema validation.
- Order graph constraints.
- Order update constraints MVP.
- CancelOrder.
- State/factsheet/connection ingestion.

### Task 7.2: Documentar MQTT topics

**Files:**
- Update: `docs/mqtt-topics.md`

Incluir exemplos:

- `vda5050/v3/ResearchBot/RB001/state`
- `vda5050/v3/ResearchBot/RB001/order`
- payloads mínimos.

### Task 7.3: E2E com Docker Compose

**Objective:** Provar que pesquisador consegue rodar tudo.

**Command:**

```bash
docker compose up --build
```

**Verification manual:**

- `http://localhost:8000/health` retorna OK.
- `http://localhost:8000/docs` abre OpenAPI.
- `http://localhost:5173` abre UI.
- Mosquitto aceita publish/subscribe local.

### Task 7.4: Playwright smoke test

**Files:**
- Create: `frontend/tests/e2e/smoke.spec.ts`

**Test:**

- Abre Dashboard.
- Navega para Robots.
- Navega para Map.
- Navega para Missions.

### Task 7.5: CI GitHub Actions

**Files:**
- Create: `.github/workflows/ci.yml`

**Jobs:**

- backend lint/test.
- frontend lint/test/build.
- docker compose config.

---

## 8. Futuro client/simulador de teste

Planejar após MVP, mas deixar arquitetura preparada.

### Objetivo

Aplicação separada que simula um ou mais mobile robots VDA 5050 para pesquisa e testes.

### Local sugerido

```text
clients/python-simulator/
```

### Features v0.2

- Conectar no Mosquitto.
- Publicar `connection` online/offline com Last Will.
- Publicar `factsheet`.
- Receber `order`.
- Validar `order`.
- Simular progresso por nodes/edges.
- Publicar `state` e `visualization` periodicamente.
- Responder a `cancelOrder`.
- Config YAML para múltiplos robôs.

### Benefício

- Teste reproduzível sem robô real.
- Demonstração didática do fleet manager.
- Base para experimentos de roteamento/alocação.

---

## 9. Estratégia de testes

### Backend

- Unitários:
  - VDA validator.
  - Topic parser.
  - Order builder.
  - Route planner.
  - Mission state machine.
- Integração:
  - PostgreSQL.
  - MQTT Mosquitto.
  - APIs FastAPI.
- Contrato:
  - Payloads aceitos pelos schemas VDA.
  - Payloads inválidos geram logs/erros corretos.

### Frontend

- Unit/component:
  - tabelas;
  - forms;
  - order preview;
  - map canvas helpers.
- E2E:
  - smoke navigation;
  - criar mapa;
  - criar missão;
  - dispatch usando backend fake ou stack real.

### Docker

- `docker compose config`.
- `docker compose up --build`.
- Healthchecks para Postgres, Mosquitto, backend e frontend.

---

## 10. Riscos e tradeoffs

1. **VDA 5050 v3.0.0 é a versão-alvo e introduz tópicos opcionais novos (`zoneSet`, `responses`).**
   - Mitigação: pinzar tag `3.0.0`, implementar validação para todos os schemas e tratar `zoneSet`/`responses` como opcionais no MVP.

2. **VDA 5050 define interface, não todo o algoritmo de fleet management.**
   - Mitigação: separar compliance VDA de módulos de pesquisa: routing, allocation, traffic.

3. **Traffic control completo é complexo.**
   - Mitigação: MVP com shortest path e visualização; v0.2 com reservas e deadlock.

4. **Mapa indoor não segue necessariamente latitude/longitude.**
   - Mitigação: usar canvas/grafo métrico, não mapas geográficos por padrão.

5. **Sem client/simulador no MVP dificulta demonstração.**
   - Mitigação: criar testes MQTT e fixtures; implementar simulador logo após MVP.

6. **Pydantic models completos VDA podem ficar grandes.**
   - Mitigação: usar JSON Schema como fonte de validação; criar Pydantic apenas para DTOs internos e payloads principais quando necessário.

---

## 11. Open questions

1. Licença desejada: MIT, Apache-2.0 ou BSD-3-Clause?
2. Nome final do projeto continua `TARS`?
3. Idioma principal da documentação: inglês, português ou ambos?
4. O MVP deve aceitar apenas VDA 5050 v3.0.0 ou manter uma camada de compatibilidade futura para v2.1?
5. Mapas devem ser criados manualmente no MVP ou importar algum formato específico desde o início?
6. O algoritmo de alocação inicial será manual ou automático simples por menor distância?
7. Há algum robô/simulador real que deve ser usado como referência de integração?

---

## 12. Ordem recomendada de execução

1. Phase 0: reset e docs iniciais.
2. Phase 1: Docker + backend base.
3. Phase 2: VDA core.
4. Phase 3: DB/services.
5. Phase 4: MQTT runtime.
6. Phase 5: APIs/eventos.
7. Phase 6: frontend.
8. Phase 7: compliance/docs/QA.
9. Depois: client/simulador v0.2.

A cada task:

```bash
git status --short
# implementar apenas a task
# rodar verificação da task
git add <files>
git commit -m "<type>: <description>"
```

---

## 13. Definition of Done do MVP

O MVP está pronto quando:

- `docker compose up --build` sobe a stack completa.
- Backend responde `/health` e `/docs`.
- Frontend abre e navega pelas telas principais.
- Schemas VDA 5050 v3.0.0 estão versionados e documentados.
- Backend valida `order`, `instantActions`, `state`, `connection`, `factsheet`, `visualization`, `zoneSet` e `responses`.
- Backend recebe mensagens MQTT de `state` e atualiza robôs.
- Backend publica `order` válido em tópico VDA.
- UI permite criar mapa simples, criar missão e despachar ordem.
- Logs MQTT mostram inbound/outbound e erros de validação.
- Testes backend e frontend passam.
- `docs/vda5050-compliance.md` mostra status real do que foi implementado.

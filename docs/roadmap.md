# Development Roadmap

The operational v1 fleet-manager baseline and its Docker E2E are complete. The items below are
explicitly deferred until post-v1 development begins.

## Post-v1 map interoperability

- Versioned canonical graph import/export format.
- Transactional bulk import with validation and dry-run.
- JSON and CSV adapters, followed by optional GeoJSON and ROS/ROS2 adapters.
- Coordinate-system, unit, origin, floor, and transform metadata.
- Map revisions, clone, rollback, and safe deletion rules.
- Reproducible exports for research datasets and experiments.

## Post-v1 pluggable route planning

- A transport- and persistence-independent `RoutePlanner` contract.
- Planner registry with selection by configuration or mission.
- Dijkstra baseline plus A*, time, energy, and multi-objective costs.
- Planning context for blocks, reservations, battery, and robot constraints.
- Algorithm plugins with persisted parameters, seed, cost, and execution time.
- Shared planner conformance tests and versioned benchmark scenarios.
- Later evolution toward multi-robot planning, congestion, and deadlock avoidance.

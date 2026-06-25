from dataclasses import dataclass
from typing import Any

from tars_robot_simulator.payloads import (
    RobotIdentity,
    build_connection_payload,
    build_factsheet_payload,
    build_state_payload,
)
from tars_robot_simulator.topics import build_topic


@dataclass(frozen=True)
class Publication:
    topic: str
    payload: dict[str, Any]
    qos: int = 0
    retain: bool = False


class SimulatedRobot:
    def __init__(self, identity: RobotIdentity, *, initial_state_of_charge: float = 80.0) -> None:
        self.identity = identity
        self.header_id = 0
        self.state_of_charge = initial_state_of_charge
        self.current_order_id = ""
        self.current_order_update_id = 0

    def startup_publications(self) -> list[Publication]:
        return [
            self.connection_publication("ONLINE"),
            self.factsheet_publication(),
            self.state_publication(),
        ]

    def connection_publication(self, connection_state: str = "ONLINE") -> Publication:
        return Publication(
            topic=build_topic(self.identity, "connection"),
            payload=build_connection_payload(
                self.identity,
                header_id=self._next_header_id(),
                connection_state=connection_state,  # type: ignore[arg-type]
            ),
            qos=1,
            retain=True,
        )

    def factsheet_publication(self) -> Publication:
        return Publication(
            topic=build_topic(self.identity, "factsheet"),
            payload=build_factsheet_payload(self.identity, header_id=self._next_header_id()),
        )

    def state_publication(self) -> Publication:
        return Publication(
            topic=build_topic(self.identity, "state"),
            payload=build_state_payload(
                self.identity,
                header_id=self._next_header_id(),
                state_of_charge=self.state_of_charge,
                order_id=self.current_order_id,
                order_update_id=self.current_order_update_id,
            ),
        )

    def apply_order(self, payload: dict[str, Any]) -> None:
        self.current_order_id = str(payload.get("orderId", ""))
        self.current_order_update_id = int(payload.get("orderUpdateId", 0))

    def _next_header_id(self) -> int:
        self.header_id += 1
        return self.header_id

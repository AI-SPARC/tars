"""Exercise a complete fleet-control -> robot -> fleet-control order cycle."""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

API_BASE = os.getenv("TARS_API_BASE_URL", "http://localhost:8000/api/v1")
SERIAL_NUMBER = os.getenv("TARS_E2E_ROBOT_SERIAL", "RB-SIM-001")


def request(path: str, payload: dict[str, Any] | None = None) -> Any:
    data = json.dumps(payload).encode() if payload is not None else None
    method = "POST" if payload is not None else "GET"
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.load(response)


def wait_for_robot() -> dict[str, Any]:
    for _ in range(30):
        try:
            robots = request("/robots")
            robot = next(
                (item for item in robots if item["serialNumber"] == SERIAL_NUMBER), None
            )
            if robot is not None:
                return robot
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(1)
    raise RuntimeError(f"Simulator robot {SERIAL_NUMBER} was not discovered")


def main() -> None:
    robot = wait_for_robot()
    graph = request("/maps", {"name": "Automated E2E Lab"})
    request(f"/maps/{graph['id']}/nodes", {"nodeKey": "A", "x": 0, "y": 0})
    request(f"/maps/{graph['id']}/nodes", {"nodeKey": "B", "x": 2, "y": 0})
    request(
        f"/maps/{graph['id']}/edges",
        {
            "edgeKey": "A-B",
            "fromNodeKey": "A",
            "toNodeKey": "B",
            "distance": 2,
        },
    )
    mission = request(
        "/missions",
        {
            "mapId": graph["id"],
            "assignedRobotId": robot["id"],
            "startNodeKey": "A",
            "goalNodeKey": "B",
            "priority": 0,
        },
    )
    dispatched = request(f"/missions/{mission['id']}/dispatch", {})
    if not dispatched["accepted"]:
        raise RuntimeError(f"Mission dispatch was rejected: {dispatched}")

    for _ in range(15):
        state = request(f"/robots/{robot['id']}/state/latest")
        if state["orderId"] == mission["id"]:
            print(
                json.dumps(
                    {
                        "missionId": mission["id"],
                        "topic": dispatched["topic"],
                        "stateOrderId": state["orderId"],
                    }
                )
            )
            return
        time.sleep(1)
    raise RuntimeError("Simulator state did not acknowledge the dispatched order")


if __name__ == "__main__":
    main()

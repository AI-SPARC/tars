import argparse
import asyncio
import json
import logging
import sys

import aiomqtt

from tars_robot_simulator.payloads import RobotIdentity
from tars_robot_simulator.simulator import Publication, SimulatedRobot
from tars_robot_simulator.topics import subscription_topics

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TARS VDA 5050 v3.0.0 robot simulator")
    parser.add_argument("--mqtt-host", default="localhost")
    parser.add_argument("--mqtt-port", type=int, default=1883)
    parser.add_argument("--manufacturer", default="ResearchBot")
    parser.add_argument("--serial-number", default="RB-SIM-001")
    parser.add_argument("--state-interval", type=float, default=2.0)
    parser.add_argument("--once", action="store_true", help="Publish startup messages and exit")
    return parser


def main() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    identity = RobotIdentity(args.manufacturer, args.serial_number)
    robot = SimulatedRobot(identity)
    asyncio.run(
        run_simulator(
            robot,
            mqtt_host=args.mqtt_host,
            mqtt_port=args.mqtt_port,
            state_interval=args.state_interval,
            once=args.once,
        )
    )


async def run_simulator(
    robot: SimulatedRobot,
    *,
    mqtt_host: str,
    mqtt_port: int,
    state_interval: float,
    once: bool = False,
) -> None:
    async with aiomqtt.Client(hostname=mqtt_host, port=mqtt_port) as client:
        for topic in subscription_topics(robot.identity):
            await client.subscribe(topic)
            logger.info("Subscribed to %s", topic)

        for publication in robot.startup_publications():
            await publish(client, publication)

        if once:
            return

        await asyncio.gather(
            publish_state_forever(client, robot, state_interval),
            consume_commands(client, robot),
        )


async def publish_state_forever(
    client: aiomqtt.Client, robot: SimulatedRobot, state_interval: float
) -> None:
    while True:
        await asyncio.sleep(state_interval)
        await publish(client, robot.state_publication())


async def consume_commands(client: aiomqtt.Client, robot: SimulatedRobot) -> None:
    async for message in client.messages:
        try:
            payload = json.loads(message.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            logger.warning("Ignoring invalid command payload on %s: %s", message.topic, exc)
            continue
        topic = str(message.topic)
        logger.info("Received %s: %s", topic, payload)
        if topic.endswith("/order"):
            robot.apply_order(payload)
            await publish(client, robot.state_publication())
        elif topic.endswith("/instantActions"):
            robot.apply_instant_actions(payload)
            await publish(client, robot.state_publication())


async def publish(client: aiomqtt.Client, publication: Publication) -> None:
    payload = json.dumps(publication.payload, separators=(",", ":"))
    await client.publish(
        publication.topic,
        payload=payload,
        qos=publication.qos,
        retain=publication.retain,
    )
    logger.info("Published %s", publication.topic)


if __name__ == "__main__":
    main()

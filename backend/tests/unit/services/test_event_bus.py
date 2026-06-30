from app.services.event_bus import EventBus


async def test_event_bus_broadcasts_an_independent_copy_to_each_subscriber() -> None:
    event_bus = EventBus()

    async with event_bus.subscribe() as first, event_bus.subscribe() as second:
        published = event_bus.publish(
            "robot.state.updated",
            robot_id="robot-1",
            payload={"battery": 80},
        )

        assert await first.get() == published
        assert await second.get() == published
        assert published.as_message()["robotId"] == "robot-1"
        assert event_bus.subscriber_count == 2

    assert event_bus.subscriber_count == 0


async def test_event_bus_drops_oldest_event_for_a_slow_subscriber() -> None:
    event_bus = EventBus(subscriber_buffer_size=2)

    async with event_bus.subscribe() as events:
        event_bus.publish("event.1")
        event_bus.publish("event.2")
        event_bus.publish("event.3")

        assert (await events.get()).type == "event.2"
        assert (await events.get()).type == "event.3"

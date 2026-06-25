from app.mqtt.worker import build_subscription_filter


def test_build_subscription_filter_targets_vda5050_v3_topics() -> None:
    assert build_subscription_filter() == "vda5050/v3/+/+/+"


def test_build_subscription_filter_uses_custom_interface_and_version() -> None:
    assert build_subscription_filter("custom", "v9") == "custom/v9/+/+/+"

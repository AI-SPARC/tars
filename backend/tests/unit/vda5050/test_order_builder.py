from app.vda5050.order_builder import RouteEdge, RouteNode, build_order
from app.vda5050.validator import validate_message


def test_build_order_assigns_continuous_node_edge_sequence_ids() -> None:
    order = build_order(
        manufacturer="ResearchBot",
        serial_number="RB001",
        header_id=7,
        order_id="mission-1",
        nodes=[
            RouteNode(node_id="A", x=0.0, y=0.0, theta=0.0, map_id="lab"),
            RouteNode(node_id="B", x=1.0, y=0.0, theta=0.0, map_id="lab"),
        ],
        edges=[RouteEdge(edge_id="A-B", start_node_id="A", end_node_id="B")],
    )

    assert [node["sequenceId"] for node in order["nodes"]] == [0, 2]
    assert [edge["sequenceId"] for edge in order["edges"]] == [1]
    assert order["nodes"][0]["released"] is True
    assert order["edges"][0]["released"] is True
    assert validate_message("order", order).valid is True


def test_build_order_allows_single_node_order_with_no_edges() -> None:
    order = build_order(
        manufacturer="ResearchBot",
        serial_number="RB001",
        header_id=8,
        order_id="mission-2",
        nodes=[RouteNode(node_id="A", x=0.0, y=0.0, theta=0.0, map_id="lab")],
        edges=[],
    )

    assert len(order["nodes"]) == 1
    assert order["edges"] == []
    assert validate_message("order", order).valid is True

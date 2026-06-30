"""initial fleet manager schema

Revision ID: 0001_initial_fleet_schema
Revises:
Create Date: 2026-06-25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0001_initial_fleet_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def json_type() -> sa.JSON:
    return sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def timestamp_column(name: str) -> sa.Column:
    return sa.Column(name, sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)


def upgrade() -> None:
    op.create_table(
        "robots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("manufacturer", sa.String(length=128), nullable=False),
        sa.Column("serial_number", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=True),
        sa.Column("protocol_version", sa.String(length=16), nullable=False),
        sa.Column("last_connection_state", sa.String(length=32), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("factsheet", json_type(), nullable=True),
        sa.Column("capabilities", json_type(), nullable=True),
        timestamp_column("created_at"),
        timestamp_column("updated_at"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("manufacturer", "serial_number", name="uq_robot_identity"),
    )
    op.create_table(
        "robot_state_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("robot_id", sa.String(length=36), nullable=False),
        sa.Column("header_id", sa.Integer(), nullable=True),
        sa.Column("order_id", sa.String(length=128), nullable=True),
        sa.Column("order_update_id", sa.Integer(), nullable=True),
        sa.Column("last_node_id", sa.String(length=128), nullable=True),
        sa.Column("last_node_sequence_id", sa.Integer(), nullable=True),
        sa.Column("battery_charge", sa.Float(), nullable=True),
        sa.Column("operating_mode", sa.String(length=64), nullable=True),
        sa.Column("errors", json_type(), nullable=True),
        sa.Column("safety_state", json_type(), nullable=True),
        sa.Column("agv_position", json_type(), nullable=True),
        sa.Column("node_states", json_type(), nullable=True),
        sa.Column("edge_states", json_type(), nullable=True),
        sa.Column("action_states", json_type(), nullable=True),
        sa.Column("raw_payload", json_type(), nullable=False),
        timestamp_column("received_at"),
        sa.ForeignKeyConstraint(["robot_id"], ["robots.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "maps",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("floor", sa.String(length=80), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "map_nodes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("map_id", sa.String(length=36), nullable=False),
        sa.Column("node_key", sa.String(length=128), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("theta", sa.Float(), nullable=False),
        sa.Column("node_type", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["map_id"], ["maps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("map_id", "node_key", name="uq_map_node_key"),
    )
    op.create_table(
        "map_edges",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("map_id", sa.String(length=36), nullable=False),
        sa.Column("edge_key", sa.String(length=128), nullable=False),
        sa.Column("from_node_key", sa.String(length=128), nullable=False),
        sa.Column("to_node_key", sa.String(length=128), nullable=False),
        sa.Column("distance", sa.Float(), nullable=False),
        sa.Column("bidirectional", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["map_id"], ["maps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("map_id", "edge_key", name="uq_map_edge_key"),
    )
    op.create_table(
        "missions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("assigned_robot_id", sa.String(length=36), nullable=True),
        sa.Column("start_node_key", sa.String(length=128), nullable=False),
        sa.Column("goal_node_key", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        timestamp_column("created_at"),
        sa.ForeignKeyConstraint(["assigned_robot_id"], ["robots.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mqtt_message_logs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("topic", sa.String(length=500), nullable=False),
        sa.Column("message_type", sa.String(length=64), nullable=False),
        sa.Column("payload", json_type(), nullable=False),
        sa.Column("schema_valid", sa.Boolean(), nullable=False),
        timestamp_column("created_at"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("mqtt_message_logs")
    op.drop_table("missions")
    op.drop_table("map_edges")
    op.drop_table("map_nodes")
    op.drop_table("maps")
    op.drop_table("robot_state_snapshots")
    op.drop_table("robots")

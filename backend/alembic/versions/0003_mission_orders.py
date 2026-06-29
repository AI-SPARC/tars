"""add map-aware missions and persisted VDA orders

Revision ID: 0003_mission_orders
Revises: 0002_mqtt_runtime_metadata
Create Date: 2026-06-29
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0003_mission_orders"
down_revision: str | None = "0002_mqtt_runtime_metadata"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def json_type() -> sa.JSON:
    return sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def upgrade() -> None:
    op.add_column("missions", sa.Column("map_id", sa.String(length=36), nullable=True))
    op.create_foreign_key(
        "fk_missions_map_id_maps",
        "missions",
        "maps",
        ["map_id"],
        ["id"],
    )
    op.create_table(
        "mission_orders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("mission_id", sa.String(length=36), nullable=False),
        sa.Column("robot_id", sa.String(length=36), nullable=False),
        sa.Column("order_id", sa.String(length=128), nullable=False),
        sa.Column("order_update_id", sa.Integer(), nullable=False),
        sa.Column("header_id", sa.Integer(), nullable=False),
        sa.Column("payload", json_type(), nullable=False),
        sa.Column("validation_status", sa.String(length=32), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["mission_id"], ["missions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["robot_id"], ["robots.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("robot_id", "header_id", name="uq_mission_order_robot_header"),
    )


def downgrade() -> None:
    op.drop_table("mission_orders")
    op.drop_constraint("fk_missions_map_id_maps", "missions", type_="foreignkey")
    op.drop_column("missions", "map_id")

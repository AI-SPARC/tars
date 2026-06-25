"""add mqtt runtime metadata

Revision ID: 0002_mqtt_runtime_metadata
Revises: 0001_initial_fleet_schema
Create Date: 2026-06-25
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0002_mqtt_runtime_metadata"
down_revision: str | None = "0001_initial_fleet_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def json_type() -> sa.JSON:
    return sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def upgrade() -> None:
    op.add_column(
        "mqtt_message_logs",
        sa.Column("qos", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "mqtt_message_logs",
        sa.Column("retain", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "mqtt_message_logs",
        sa.Column("robot_id", sa.String(length=36), nullable=True),
    )
    op.add_column(
        "mqtt_message_logs",
        sa.Column("validation_errors", json_type(), nullable=False, server_default="[]"),
    )
    op.create_foreign_key(
        "fk_mqtt_message_logs_robot_id_robots",
        "mqtt_message_logs",
        "robots",
        ["robot_id"],
        ["id"],
    )
    op.alter_column("mqtt_message_logs", "qos", server_default=None)
    op.alter_column("mqtt_message_logs", "retain", server_default=None)
    op.alter_column("mqtt_message_logs", "validation_errors", server_default=None)


def downgrade() -> None:
    op.drop_constraint(
        "fk_mqtt_message_logs_robot_id_robots",
        "mqtt_message_logs",
        type_="foreignkey",
    )
    op.drop_column("mqtt_message_logs", "validation_errors")
    op.drop_column("mqtt_message_logs", "robot_id")
    op.drop_column("mqtt_message_logs", "retain")
    op.drop_column("mqtt_message_logs", "qos")

"""Initial migration to create tables

Revision ID: 20231027
Revises:
Create Date: 2023-10-27 00:00:00.000000
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "20231027"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dbuser",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column(
            "contact_info", sa.String(), nullable=True
        ),
        sa.Column(
            "temp_password", sa.Boolean(), nullable=True
        ),
        sa.Column(
            "roles_internal", sa.String(), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dbuser_id"), "dbuser", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_dbuser_username"),
        "dbuser",
        ["username"],
        unique=True,
    )
    op.create_table(
        "dbproject",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "responsible", sa.String(), nullable=False
        ),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "description", sa.String(), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dbproject_id"),
        "dbproject",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dbproject_name"),
        "dbproject",
        ["name"],
        unique=False,
    )
    op.create_table(
        "dbtask",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "description", sa.String(), nullable=False
        ),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column(
            "project_id", sa.Integer(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["dbproject.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dbtask_id"), "dbtask", ["id"], unique=False
    )
    op.create_table(
        "dblogentry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), nullable=False
        ),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("user", sa.String(), nullable=False),
        sa.Column(
            "project_id", sa.Integer(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["project_id"], ["dbproject.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dblogentry_id"),
        "dblogentry",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_dblogentry_id"), table_name="dblogentry"
    )
    op.drop_table("dblogentry")
    op.drop_index(op.f("ix_dbtask_id"), table_name="dbtask")
    op.drop_table("dbtask")
    op.drop_index(
        op.f("ix_dbproject_name"), table_name="dbproject"
    )
    op.drop_index(
        op.f("ix_dbproject_id"), table_name="dbproject"
    )
    op.drop_table("dbproject")
    op.drop_index(
        op.f("ix_dbuser_username"), table_name="dbuser"
    )
    op.drop_index(op.f("ix_dbuser_id"), table_name="dbuser")
    op.drop_table("dbuser")
"""create users table

Revision ID: 775aff53fe63
Revises: 065783c5d6ae
Create Date: 2023-02-28 19:36:20.232500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "775aff53fe63"
down_revision = "065783c5d6ae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False, unique=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default="now()",
        ),
    )


def downgrade() -> None:
    op.drop_table("users")

"""create posts table

Revision ID: 065783c5d6ae
Revises: 
Create Date: 2023-02-28 14:11:02.256204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "065783c5d6ae"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default="now()",
        ),
    )


def downgrade() -> None:
    op.drop_table("posts")

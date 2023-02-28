"""create likes table

Revision ID: f5e13b6d5df6
Revises: 238250eb8dd4
Create Date: 2023-02-28 22:10:15.712265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f5e13b6d5df6"
down_revision = "238250eb8dd4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "likes",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("post_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table("likes")

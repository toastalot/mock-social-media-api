"""create posts->users foreign key constraint

Revision ID: 238250eb8dd4
Revises: 775aff53fe63
Create Date: 2023-02-28 20:47:21.973339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "238250eb8dd4"
down_revision = "775aff53fe63"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")

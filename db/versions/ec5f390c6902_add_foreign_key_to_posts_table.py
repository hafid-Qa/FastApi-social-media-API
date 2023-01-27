"""add foreign-key to posts table

Revision ID: ec5f390c6902
Revises: fd48f5d60ee1
Create Date: 2023-01-27 22:01:25.034158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ec5f390c6902"
down_revision = "fd48f5d60ee1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column(
    #     "posts", sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # )
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
